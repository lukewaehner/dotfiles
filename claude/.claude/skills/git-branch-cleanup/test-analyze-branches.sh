#!/usr/bin/env bash
# Regression test for analyze-branches.sh bucketing.
#
# Builds a throwaway repo with one branch per classification case and asserts
# each lands in the expected bucket. Self-contained: no framework, no network,
# no dependency on the machine's real repos.
#
# Usage: ./test-analyze-branches.sh   (exit 0 = pass)
set -uo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ANALYZE="$SCRIPT_DIR/analyze-branches.sh"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# --- arrange: a remote, a main with one commit, and four branch shapes -------
git init --bare -q -b main "$TMP/remote"
git init -q -b main "$TMP/work"
cd "$TMP/work" || exit 1
git remote add origin "$TMP/remote"
git config user.email test@example.com
git config user.name "Test"
echo a > a.txt && git add . && git commit -qm "initial"
git push -q -u origin main

# no upstream, nothing ahead of main -> merged, nothing unpushed to protect
git branch noupstream-merged

# no upstream, one local-only commit -> real unpushed work
git checkout -q -b noupstream-unpushed
echo b > b.txt && git add . && git commit -qm "wip"

# upstream, in sync, ancestor of main
git checkout -q main
git checkout -q -b tracked-merged
git push -q -u origin tracked-merged

# upstream, ahead of it -> in-progress elsewhere
git checkout -q -b tracked-ahead
git push -q -u origin tracked-ahead
echo d > d.txt && git add . && git commit -qm "ahead of remote"

git checkout -q main

# --- act --------------------------------------------------------------------
report=$(bash "$ANALYZE" "$TMP/work" 2>&1)

# --- assert -----------------------------------------------------------------
# bucket_of <branch> -> safe | stale | active | none
bucket_of() {
  printf '%s\n' "$report" | awk -v want="$1" '
    /^### Safe to delete/   { b="safe";   next }
    /^### Stale/            { b="stale";  next }
    /^### Active/           { b="active"; next }
    $0 ~ "^  - " want " " || $0 ~ "^  - " want "$" { print b; found=1; exit }
    END { if (!found) print "none" }
  '
}

failures=0
check() {
  local branch="$1" expected="$2" actual
  actual=$(bucket_of "$branch")
  if [[ "$actual" == "$expected" ]]; then
    printf 'ok    %-22s -> %s\n' "$branch" "$actual"
  else
    printf 'FAIL  %-22s -> %s (expected %s)\n' "$branch" "$actual" "$expected"
    failures=$((failures + 1))
  fi
}

# Regression: a branch with no upstream but nothing ahead of main used to be
# parked in "active" forever, because the no-upstream guard short-circuited
# before the merge checks could run. It has no unpushed work to protect.
check noupstream-merged   safe
check noupstream-unpushed active
check tracked-merged      safe
check tracked-ahead       active

if [[ "$failures" -ne 0 ]]; then
  echo
  echo "$failures check(s) failed. Full report:"
  printf '%s\n' "$report"
  exit 1
fi

echo "all checks passed"
