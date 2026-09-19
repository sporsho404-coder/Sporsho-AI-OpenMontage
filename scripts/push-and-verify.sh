#!/usr/bin/env bash
# =============================================================================
# push-and-verify.sh — Sporsho AI x OpenMontage
#
# Pushes the EXISTING local repository to origin and verifies the result.
#
# This script does NOT create a repository, does NOT initialise git, and does
# NOT rebuild anything. It pushes the existing main branch and all existing
# history, then verifies.
#
# Usage:
#   ./scripts/push-and-verify.sh
# =============================================================================
set -uo pipefail

cd "$(dirname "$0")/.."

ORIGIN="https://github.com/sporsho404-coder/Sporsho-AI-OpenMontage.git"
UPSTREAM="https://github.com/calesthio/OpenMontage.git"

pass() { printf '  \033[32mPASS\033[0m  %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAILED=1; }
warn() { printf '  \033[33mWARN\033[0m  %s\n' "$1"; }
info() { printf '        %s\n' "$1"; }
FAILED=0

echo "=============================================================="
echo " STEP 1 — Pre-flight"
echo "=============================================================="

[ -d .git ] || { echo "ERROR: not a git repository."; exit 1; }
[ -d SPORSHO ] || { echo "ERROR: SPORSHO/ missing — wrong directory?"; exit 1; }
pass "running in the existing local repository (not a rebuild)"

git rev-parse --verify main >/dev/null 2>&1 || { echo "ERROR: no main branch."; exit 1; }
pass "branch main exists"

# Working tree clean?
if [ -z "$(git status --porcelain)" ]; then
  pass "working tree clean"
else
  warn "working tree has uncommitted changes:"
  git status --short | sed 's/^/        /'
  read -r -p "  Continue anyway? [y/N] " a
  [ "${a:-n}" = "y" ] || exit 1
fi

# Remotes
if git remote get-url origin >/dev/null 2>&1; then
  if [ "$(git remote get-url origin)" = "$ORIGIN" ]; then
    pass "origin correct"
  else
    warn "origin is $(git remote get-url origin) — resetting"
    git remote set-url origin "$ORIGIN"
    pass "origin reset to $ORIGIN"
  fi
else
  git remote add origin "$ORIGIN"
  pass "origin added"
fi

if ! git remote get-url upstream >/dev/null 2>&1; then
  git remote add upstream "$UPSTREAM"
  warn "upstream re-added"
fi
git remote set-url --push upstream DISABLED_NEVER_PUSH_TO_UPSTREAM
pass "upstream is fetch-only (push disabled)"

git branch --unset-upstream main 2>/dev/null || true
pass "main does not track upstream/main"

# AGPL preservation
if [ -f LICENSE ] && head -1 LICENSE | grep -qi "GNU AFFERO"; then
  pass "LICENSE present and is AGPL-3.0 ($(wc -l < LICENSE) lines)"
else
  fail "LICENSE missing or not AGPL-3.0"
fi

if git remote get-url upstream >/dev/null 2>&1 && \
   git rev-parse --verify upstream/main >/dev/null 2>&1; then
  if git diff --quiet upstream/main -- LICENSE; then
    pass "LICENSE byte-identical to upstream"
  else
    warn "LICENSE differs from upstream/main — verify this is intentional"
  fi
fi

echo
echo "=============================================================="
echo " STEP 2 — Exclusion audit (what must NOT be uploaded)"
echo "=============================================================="

# Secrets
SEC=$(git ls-files | grep -iE '(^|/)\.env$|\.env\.(local|prod|production|dev)|\.pem$|\.key$|\.p12$|/credentials\.json$|/token\.json$|service[-_]account.*\.json$' || true)
if [ -z "$SEC" ]; then
  pass "no secret files tracked"
else
  fail "secret files tracked:"; echo "$SEC" | sed 's/^/        /'
fi

PAT='(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'
if git grep -qIE "$PAT" -- . ':!SETUP.md' ':!scripts/*.sh' ':!docs/sporsho/GITHUB.md' 2>/dev/null; then
  fail "token-like pattern found in tracked content:"
  git grep -nIE "$PAT" -- . ':!SETUP.md' ':!scripts/*.sh' ':!docs/sporsho/GITHUB.md' 2>/dev/null | sed -n '1,5p' | sed 's/^/        /'
else
  pass "no API-key/token patterns in tracked content"
fi

if [ -f .env ]; then warn ".env exists on disk but is gitignored (verify: git check-ignore .env)"; fi

# Cache / build
if git ls-files | grep -qiE '(^|/)(__pycache__|node_modules|\.pytest_cache|\.mypy_cache|dist|build|out|target|coverage)/|\.pyc$'; then
  fail "cache/build artifacts tracked"
else
  pass "no cache or build artifacts tracked"
fi

# Media — every media file must be upstream-owned.
#
# The upstream file list is materialised ONCE into a temp file. Doing the lookup
# inside a `while read` loop would let `git ls-tree | grep` consume the loop's
# stdin and silently corrupt the comparison (classic stdin-eating bug).
MEDIA_TMP=$(mktemp) UPSTREAM_TMP=$(mktemp)
trap 'rm -f "$MEDIA_TMP" "$UPSTREAM_TMP"' EXIT

git ls-files | grep -iE '\.(mp4|mov|mkv|avi|webm|wav|flac|psd|tif|braw|r3d)$' > "$MEDIA_TMP" || true
git rev-parse --verify upstream/main >/dev/null 2>&1 \
  && git ls-tree -r upstream/main --name-only > "$UPSTREAM_TMP" || true

MEDIA_COUNT=$(grep -c . "$MEDIA_TMP" || true)
NEW_MEDIA=""
if [ -s "$UPSTREAM_TMP" ]; then
  NEW_MEDIA=$(grep -vxF -f "$UPSTREAM_TMP" "$MEDIA_TMP" || true)
else
  NEW_MEDIA=$(cat "$MEDIA_TMP")
fi

if [ -z "$NEW_MEDIA" ]; then
  pass "all ${MEDIA_COUNT} tracked media files are upstream-owned (zero user media)"
else
  fail "NEW media present that is not upstream:"
  echo "$NEW_MEDIA" | sed 's/^/        /'
fi

# Size
OVER=$(git ls-files -z | xargs -0 -I{} sh -c 'test -f "{}" && s=$(stat -c%s "{}" 2>/dev/null || stat -f%z "{}" 2>/dev/null || echo 0); [ "$s" -gt 52428800 ] && echo "{}"' 2>/dev/null || true)
if [ -z "$OVER" ]; then
  pass "no file over 50 MB (GitHub warning threshold)"
else
  fail "files over 50 MB:"; echo "$OVER" | sed 's/^/        /'
fi

echo
echo "=============================================================="
echo " STEP 3 — Push"
echo "=============================================================="
info "origin:  $(git remote get-url origin)"
info "branch:  main"
info "commits: $(git rev-list --count main)"
info "objects: $(git rev-list --objects main | wc -l)"
info "pack:    $(git count-objects -vH | awk '/size-pack/{print $2 $3}')"
echo
echo "  NOTE: no force-push. This is a normal fast-forward push of existing"
echo "        history to an empty repository."
echo

if [ "$FAILED" -ne 0 ]; then
  echo "  Pre-flight FAILED. Fix the issues above before pushing."
  exit 1
fi

read -r -p "  Push to origin/main now? [y/N] " ans
if [ "${ans:-n}" != "y" ]; then
  echo
  echo "  Aborted. Push manually when ready:"
  echo "      git push -u origin main"
  exit 0
fi

echo
if git push -u origin main; then
  pass "push succeeded"
else
  fail "push FAILED — see the error above"
  echo
  echo "  Most likely causes:"
  echo "    • No credentials. Use a Personal Access Token or SSH."
  echo "      HTTPS: git remote set-url origin https://<TOKEN>@github.com/sporsho404-coder/Sporsho-AI-OpenMontage.git"
  echo "      SSH:   git remote set-url origin git@github.com:sporsho404-coder/Sporsho-AI-OpenMontage.git"
  echo "    • The GitHub repo was initialised with a README (non-fast-forward)."
  echo "      Fix: delete and recreate the GitHub repo EMPTY, then re-run."
  exit 1
fi

echo
echo "=============================================================="
echo " STEP 4 — Post-push verification"
echo "=============================================================="

git fetch origin --quiet 2>/dev/null || true

LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "MISSING")

if [ "$LOCAL" = "$REMOTE" ]; then
  pass "origin/main == local main ($(git rev-parse --short main))"
else
  fail "origin/main ($REMOTE) != local main ($LOCAL)"
fi

if [ -z "$(git status --porcelain)" ]; then
  pass "working tree clean"
else
  fail "working tree has uncommitted changes"
fi

if git merge-base --is-ancestor upstream/main main 2>/dev/null; then
  pass "upstream history fully preserved ($(git rev-list --count upstream/main) upstream commits)"
else
  fail "upstream history NOT an ancestor of main"
fi

for d in SPORSHO SPORSHO/BRAIN SPORSHO/CLIENTS SPORSHO/MEMORY SPORSHO/QC docs/sporsho pipeline_defs tools skills .agents styles; do
  if git ls-tree -r main --name-only | grep -q "^${d}/"; then
    pass "present on remote: ${d}/"
  else
    fail "MISSING on remote: ${d}/"
  fi
done

for f in SPORSHO.md PROVENANCE.md SETUP.md LICENSE AGENT_GUIDE.md README.md; do
  if git ls-tree -r main --name-only | grep -qx "$f"; then
    pass "present on remote: ${f}"
  else
    fail "MISSING on remote: ${f}"
  fi
done

echo
echo "=============================================================="
if [ "$FAILED" -eq 0 ]; then
  echo " ALL CHECKS PASSED"
else
  echo " SOME CHECKS FAILED — review above"
fi
echo "=============================================================="
echo
echo "Manual checks that require the GitHub UI:"
echo "  [ ] Repository visibility still reads PRIVATE"
echo "  [ ] Commit count on GitHub matches: $(git rev-list --count main)"
echo "  [ ] No .env / footage / renders visible in the file tree"
echo
echo "Repository: https://github.com/sporsho404-coder/Sporsho-AI-OpenMontage"

exit $FAILED
