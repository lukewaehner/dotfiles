"""ptpython configuration.

Stowed to ~/.config/ptpython/config.py. ptpython reads this once, at startup,
and hands the REPL object to `configure()` below. Everything set here is also
reachable at runtime through the F2 menu — but changes made there live only for
that session, so this file is the source of truth.

Written against ptpython 3.0.x / prompt_toolkit 3.0.x.
Reference: https://github.com/prompt-toolkit/ptpython
"""

from __future__ import annotations

import subprocess
import sys

from prompt_toolkit.filters import vi_insert_mode
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from ptpython.layout import CompletionVisualisation
from ptpython.python_input import CompletePrivateAttributes, PythonInput

__all__ = ["configure"]

# Pygments style names, closest available match to tokyonight night/day (the
# theme every other tool in these dotfiles uses). Alternatives worth trying:
# dark  — one-dark, nord, material, dracula, gruvbox-dark
# light — solarized-light, gruvbox-light, paraiso-light, xcode
CODE_STYLE_DARK = "night-owl"
CODE_STYLE_LIGHT = "tango"


def _is_dark_appearance() -> bool:
    """Best-effort read of the current macOS appearance.

    theme-switch.sh can't drive ptpython the way it drives tmux or starship —
    ptpython resolves its style at startup and offers no live reload — so the
    REPL samples the appearance itself when it launches. Anything unexpected
    (Linux, `defaults` missing, a slow or failing call) falls back to dark.
    """
    if sys.platform != "darwin":
        return True

    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=1,
        )
    except (OSError, subprocess.SubprocessError):
        return True

    # In light mode the key is absent entirely, so `defaults` exits non-zero.
    return result.stdout.strip() == "Dark"


def configure(repl: PythonInput) -> None:
    # ── Editing mode ──────────────────────────────────────────────────────────
    # zsh is deliberately pinned to emacs keys (see zsh/.zshrc), but the REPL is
    # where multi-line editing actually happens, so it gets vi keys.
    repl.vi_mode = True

    # Land in insert mode on a fresh prompt — typing is the common case — but
    # remember the mode across accepted lines, so a run of navigation-mode edits
    # doesn't get interrupted.
    repl.vi_start_in_navigation_mode = False
    repl.vi_keep_last_used_mode = True

    # The one unambiguous signal for which mode you're in.
    repl.cursor_shape_config = "Modal (vi)"

    # ── Completion ────────────────────────────────────────────────────────────
    repl.complete_while_typing = True
    repl.completion_visualisation = CompletionVisualisation.MULTI_COLUMN
    repl.completion_menu_scroll_offset = 1
    repl.enable_fuzzy_completion = True

    # Dunder and _private attributes only surface once nothing public matches.
    repl.complete_private_attributes = CompletePrivateAttributes.IF_NO_PUBLIC

    # Completes dict keys and attributes by evaluating the expression to the
    # left of the cursor — the reason `df["` completes column names. It really
    # does run that code, so drop to False when poking at objects whose
    # properties have side effects.
    repl.enable_dictionary_completion = True

    # Readline-style prefix search on ↑/↓. Mutually exclusive with
    # complete_while_typing in ptpython; auto-suggest covers the same ground.
    repl.enable_history_search = False

    # ── Suggestions and signatures ────────────────────────────────────────────
    # Fish-style ghost text from history, accepted with →.
    repl.enable_auto_suggest = True

    # Call signature and docstring of whatever you're calling, resolved by jedi
    # in a background thread.
    repl.show_signature = True
    repl.show_docstring = True

    # ── Input ─────────────────────────────────────────────────────────────────
    repl.enable_input_validation = True

    # Enter accepts on the second press for multi-line blocks; Meta+Enter always
    # accepts. Keep the hint visible — it's the one non-obvious key in the REPL.
    repl.accept_input_on_enter = 2
    repl.show_meta_enter_message = True

    # v in navigation mode (C-x C-e in insert) opens the buffer in $EDITOR.
    repl.enable_open_in_editor = True

    # C-z suspends the REPL to the background.
    repl.enable_system_bindings = True

    # Bracketed paste is detected automatically; the manual paste-mode toggle
    # (F6) stays off so indentation still works while typing.
    repl.paste_mode = False

    # ── Output ────────────────────────────────────────────────────────────────
    repl.enable_syntax_highlighting = True
    repl.highlight_matching_parenthesis = True
    repl.wrap_lines = True

    # Syntax-highlight repr output, and page anything taller than the window
    # instead of blowing away the scrollback.
    repl.enable_output_formatting = True
    repl.enable_pager = True

    repl.insert_blank_line_after_output = True
    repl.insert_blank_line_after_input = False

    # ── Chrome ────────────────────────────────────────────────────────────────
    repl.show_status_bar = True
    repl.show_line_numbers = False
    repl.show_sidebar_help = True
    repl.prompt_style = "classic"  # >>> — "ipython" gives In [1]: instead.

    # Mouse support would capture scroll and drag-select, which costs terminal
    # text selection and native scrollback. Not worth it.
    repl.enable_mouse_support = False

    # Ctrl-D exits without a prompt; the shell is cheap to restart.
    repl.confirm_exit = False

    repl.title = "ptpython"

    # ── Colors ────────────────────────────────────────────────────────────────
    repl.use_code_colorscheme(
        CODE_STYLE_DARK if _is_dark_appearance() else CODE_STYLE_LIGHT
    )

    # ── Key bindings ──────────────────────────────────────────────────────────
    # vi insert mode drops the two line-motion keys that are pure muscle memory
    # from an emacs-keymap shell. Restore them; the rest of insert mode is
    # already emacs-ish (C-w, C-u, C-k).

    @repl.add_key_binding("c-a", filter=vi_insert_mode)
    def _beginning_of_line(event: KeyPressEvent) -> None:
        buffer = event.current_buffer
        buffer.cursor_position += buffer.document.get_start_of_line_position()

    @repl.add_key_binding("c-e", filter=vi_insert_mode)
    def _end_of_line(event: KeyPressEvent) -> None:
        buffer = event.current_buffer
        buffer.cursor_position += buffer.document.get_end_of_line_position()
