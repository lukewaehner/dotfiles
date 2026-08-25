#!/usr/bin/env bash
# git-branch-cleanup: categorize local branches as safe-to-delete, stale, or active.
#
# Read-only. Never deletes or modifies anything — it fetches (to get an
# accurate view of remote state) and prints a report.
#
# Usage: analyze-branches.sh [--stale-days N] [--behind-threshold N] [repo-path ...]
#   --stale-days N        days since last commit before an unmerged branch is
#                          flagged stale (default 30)
#   --behind-threshold N  commits behind main before an unmerged branch is
#                          flagged stale regardless of age (default 50)
#   repo-path ...         one or more repo paths (default: current directory)
set -uo pipefail

STALE_DAYS=30
BEHIND_THRESHOLD=50
REPOS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stale-days) STALE_DAYS="$2"; shift 2 ;;
    --behind-threshold) BEHIND_THRESHOLD="$2"; shift 2 ;;
    *) REPOS+=("$1"); shift ;;
  esac
done
[[ ${#REPOS[@]} -eq 0 ]] && REPOS=(".")

has_gh() { command -v gh >/dev/null 2>&1; }

analyze_repo() {
  local repo="$1"
  local name
  name=$(basename "$(cd "$repo" && pwd)")
  echo "## $name ($repo)"

  (
    cd "$repo" || exit 1

    git fetch --all --prune --quiet 2>/dev/null

    local main=""
    main=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')
    if [[ -z "$main" ]]; then
      git show-ref --verify --quiet refs/heads/main && main=main
    fi
    if [[ -z "$main" ]]; then
      git show-ref --verify --quiet refs/heads/master && main=master
    fi
    if [[ -z "$main" ]]; then
      echo "  (couldn't determine default branch, skipping)"
      exit 0
    fi

    local safe=() stale=() active=()

    while IFS= read -r branch; do
      [[ "$branch" == "$main" ]] && continue

      local upstream=""
      upstream=$(git rev-parse --abbrev-ref --symbolic-full-name "${branch}@{upstream}" 2>/dev/null || true)

      if [[ -z "$upstream" ]]; then
        active+=("$branch — no remote tracking branch, review manually")
        continue
      fi

      local counts ahead_remote behind_remote
      counts=$(git rev-list --left-right --count "${branch}...${upstream}" 2>/dev/null || echo "0 0")
      ahead_remote=$(echo "$counts" | awk '{print $1}')
      behind_remote=$(echo "$counts" | awk '{print $2}')

      if [[ "$ahead_remote" != "0" || "$behind_remote" != "0" ]]; then
        active+=("$branch — not in sync with $upstream (ahead $ahead_remote / behind $behind_remote), likely in progress, skipped")
        continue
      fi

      if git merge-base --is-ancestor "$branch" "$main" 2>/dev/null; then
        safe+=("$branch — fully merged into $main (direct ancestor)")
        continue
      fi

      local cherry unmatched
      cherry=$(git cherry "$main" "$branch" 2>/dev/null || true)
      unmatched=$(printf '%s\n' "$cherry" | grep -c '^+' || true)

      if [[ -n "$cherry" && "$unmatched" -eq 0 ]]; then
        safe+=("$branch — all commits patch-equivalent in $main (rebase-merged, SHAs differ)")
        continue
      fi

      local pr_merged=""
      if has_gh; then
        pr_merged=$(gh pr list --state merged --search "head:${branch}" --json number --jq '.[0].number' 2>/dev/null || true)
      fi

      if [[ -n "$pr_merged" ]]; then
        safe+=("$branch — merged via PR #$pr_merged (likely squash-merged, patch-ids don't match)")
        continue
      fi

      local last_epoch days_old behind_main
      last_epoch=$(git log -1 --format=%ct "$branch")
      days_old=$(( ( $(date +%s) - last_epoch ) / 86400 ))
      behind_main=$(git rev-list --count "${branch}..${main}")

      if [[ "$days_old" -ge "$STALE_DAYS" || "$behind_main" -ge "$BEHIND_THRESHOLD" ]]; then
        stale+=("$branch — last commit ${days_old}d ago, ${behind_main} commits behind $main, no merge/PR record found")
      else
        active+=("$branch — unmerged but recent (${days_old}d old, ${behind_main} behind $main)")
      fi
    done < <(git for-each-ref --format='%(refname:short)' refs/heads/)

    echo "### Safe to delete (high confidence)"
    if [[ ${#safe[@]} -eq 0 ]]; then echo "  none"; else printf '  - %s\n' "${safe[@]}"; fi
    echo "### Stale / possibly abandoned (review before deleting)"
    if [[ ${#stale[@]} -eq 0 ]]; then echo "  none"; else printf '  - %s\n' "${stale[@]}"; fi
    echo "### Active (do not touch)"
    if [[ ${#active[@]} -eq 0 ]]; then echo "  none"; else printf '  - %s\n' "${active[@]}"; fi
  )
}

for repo in "${REPOS[@]}"; do
  analyze_repo "$repo"
  echo
done
