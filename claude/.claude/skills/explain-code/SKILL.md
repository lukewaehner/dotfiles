---
name: explain-code
description: Explains a piece of code line by line, tracing it through the real codebase. Use when the user pastes code or names a function/file/PR and asks "explain this", "what does this do", "walk me through", or asks what a callback, hook, prop or type is. Especially for React/TypeScript - callbacks, props, hooks, memo, native vs custom events, types.
---

# Explain Code

The goal is understanding, not a summary. Explain the code that actually exists,
in the order it runs, and name every call, callback, hook and type the reader
meets on the way.

## 1. Find the real source first

Never explain a pasted snippet from the paste alone.

- Search the repo for the function and its helpers. If they are not on the
  current branch, the code probably lives in a PR or another branch: ask, or
  check `gh pr list` / `gh pr diff <n>` / `git show <branch>:<path>`.
  (zsh: quote `"${B}:path"` - `$B:w...` is a zsh modifier.)
- Read the callers, the callees, the types, and the state it touches. A
  function that calls `onCommit` is not explained until `onCommit` is.
- If something is still unknown, say what you assumed, in one line.

## 2. First answer: what it does, then line by line

Open with two or three sentences: what the code is for and the decision it
makes. Then walk it in **execution order**, not file order:

1. **Where the data comes from** - the builder/selector/fetch that produces the
   values the code reads. Point out fields a PR added and why.
2. **State and hooks in the owner** - each `useState`, `useCallback`,
   `useMemo`, `useEffect`, `useRef`: what it holds, what changes it, what reads
   it. Say *why* the hook is there (e.g. `useCallback([])` keeps a stable
   identity so a `memo` child doesn't re-render).
3. **The wiring** - the JSX where the parent passes props to the child. Show
   the prop name next to the function bound to it (`onEdit={startEdit}`).
4. **Inside the child** - derived booleans, then each element and its
   handlers.
5. **The function asked about** - one short code block per line or small group
   of lines, each followed by a plain-language explanation of that line.
6. **Back out** - what the call it makes does on the other side, until state
   settles.

Use `file:line` references so every step is clickable. Quote code exactly; do
not paraphrase it inside a code block.

### Always name, for React/TypeScript

- **Native vs custom.** `onClick`/`onBlur`/`onKeyDown` on lowercase DOM elements
  are React-wired browser events with an event object. `onEdit`/`onCommit` on a
  capitalised component are ordinary function props the author named in the
  `onX` style - say where their type is declared.
- **Prop aliasing.** A prop is a second name for the parent's function, not a
  further call: `onEdit` *is* `startEdit`. Draw the chain as
  `click → onClick handler → onEdit(...) ≡ startEdit(...) → setState`.
- **Callback vs handler.** The prop type is the slot (the callback contract);
  the parent's function is the handler that fills it.
- **Controlled vs uncontrolled** inputs (`value` vs `defaultValue`), `memo`,
  updater-form setters (`setX(prev => ...)`), copying objects for immutability.
- **TypeScript syntax** that trips people: `!` non-null assertion, `??`, `?.`,
  indexed access types (`RowProps["onCommit"]`), unions like
  `"px" | "maxDate"`, `Extract<>`.

## 3. Close with review notes, if any

After the walkthrough, a short "worth raising" list: misleading comments,
order-dependent branches, pre-existing hazards the change touches. Mark what you
verified and what you didn't - never state an unchecked browser/framework
behaviour as fact.

## 4. Follow-up questions: short and direct

Once the walkthrough exists, follow-ups ("what are these callbacks?", "is that
native?", "so X calls Y?") get short answers:

- Lead with yes/no or the one-line answer.
- If the user's model is nearly right, confirm what's right and fix the one
  wrong piece gently (e.g. "close, but there's no second call - `onEdit` is
  `startEdit`").
- A small table or a one-line chain beats paragraphs. Don't repeat the full
  walkthrough.

## Style

- Plain words; define a term the first time it appears.
- Small code blocks, each followed by its explanation - never a wall of code
  then a wall of prose.
- Don't pad with generic React tutorials; explain *this* code's use of the
  concept.
