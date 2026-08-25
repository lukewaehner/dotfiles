#!/usr/bin/env bash
# week-summarizer: summarize feat/fix/ci/refactor commits from the last week
# (or a custom window), across every branch, grouped by module.
#
# Read-only. Never touches history — only git log / diff-tree reads.
#
# Usage: collect-week.sh [--since "<git date expression>"] [repo-path ...]
#   --since EXPR   git --since expression for the commit window (default: "7 days ago")
#   repo-path ...  one or more repo paths (default: current directory)
set -uo pipefail

SINCE="7 days ago"
REPOS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    *) REPOS+=("$1"); shift ;;
  esac
done
[[ ${#REPOS[@]} -eq 0 ]] && REPOS=(".")

# Conventional-commit types this report surfaces. Others (docs, test, chore,
# style, build, perf, ...) are deliberately left out of the summary.
WANTED_TYPES="feat fix ci refactor"
TYPE_ORDER="feat fix refactor ci"

is_wanted() {
  local t
  for t in $WANTED_TYPES; do
    [[ "$1" == "$t" ]] && return 0
  done
  return 1
}

# type(scope): desc  /  type(scope)!: desc  /  type: desc  /  type!: desc
CONVENTIONAL_COMMIT_RE='^([a-zA-Z]+)(\(([^)]+)\))?!?:[[:space:]](.*)$'

# Best-effort module name for a commit with no conventional-commit scope: the
# most common top-level directory among its changed files. Callers should
# treat this as a hint, not ground truth — override it when the diff makes a
# more meaningful module name obvious.
infer_module() {
  local hash="$1"
  git diff-tree --no-commit-id --name-only -r "$hash" 2>/dev/null \
    | awk -F/ '{print $1}' \
    | sort | uniq -c | sort -rn \
    | head -1 | awk '{$1=""; sub(/^ /, ""); print}'
}

summarize_repo() {
  local repo="$1"

  if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "# $repo"
    echo
    echo "- not a git repository, skipped"
    echo
    return
  fi

  local name
  name=$(basename "$(cd "$repo" && pwd)")
  echo "# $name"
  echo

  local rows=()
  while IFS=$'\x1f' read -r hash subject; do
    [[ -z "$hash" ]] && continue
    local type scope desc module
    if [[ "$subject" =~ $CONVENTIONAL_COMMIT_RE ]]; then
      type=$(printf '%s' "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
      scope="${BASH_REMATCH[3]}"
      desc="${BASH_REMATCH[4]}"
    else
      continue  # not a conventional-commit subject; nothing to categorize
    fi
    is_wanted "$type" || continue
    module="$scope"
    [[ -z "$module" ]] && module=$(cd "$repo" && infer_module "$hash")
    [[ -z "$module" ]] && module="(unscoped)"
    rows+=("${module}"$'\x1f'"${type}"$'\x1f'"${desc}"$'\x1f'"${hash:0:8}")
  done < <(cd "$repo" && git log --all --no-merges --since="$SINCE" --pretty=format:'%H%x1f%s')

  if [[ ${#rows[@]} -eq 0 ]]; then
    echo "- no feat/fix/ci/refactor commits in the last window ($SINCE)"
    echo
    return
  fi

  local modules=()
  local row
  for row in "${rows[@]}"; do
    modules+=("${row%%$'\x1f'*}")
  done
  local uniq_modules
  uniq_modules=$(printf '%s\n' "${modules[@]}" | sort -u)

  local m t rmod rtype rdesc rhash
  while IFS= read -r m; do
    echo "- **$m**"
    for t in $TYPE_ORDER; do
      for row in "${rows[@]}"; do
        IFS=$'\x1f' read -r rmod rtype rdesc rhash <<< "$row"
        if [[ "$rmod" == "$m" && "$rtype" == "$t" ]]; then
          echo "  - $rtype: $rdesc ($rhash)"
        fi
      done
    done
  done <<< "$uniq_modules"
  echo
}

for repo in "${REPOS[@]}"; do
  summarize_repo "$repo"
done
