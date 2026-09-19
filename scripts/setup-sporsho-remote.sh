#!/usr/bin/env bash
# =============================================================================
# Sporsho AI — one-shot remote setup
#
# Adds your GitHub repo as `origin` and pushes the prepared history.
# `upstream` is already configured and pointing at calesthio/OpenMontage.
#
# PREREQUISITE: create the PRIVATE repo on GitHub FIRST:
#   https://github.com/new
#     Name:       Sporsho-AI-OpenMontage
#     Visibility: Private          <-- IMPORTANT (AGPL-3.0; see docs/sporsho/INTEGRATION.md)
#     Do NOT initialise with README/.gitignore/licence — this repo already has history.
#
# Usage:
#   ./scripts/setup-sporsho-remote.sh git@github.com:YOUR_USERNAME/Sporsho-AI-OpenMontage.git
# =============================================================================
set -euo pipefail

REPO_URL="${1:-}"
if [ -z "$REPO_URL" ]; then
  echo "Usage: $0 <git-remote-url>"
  echo "Example: $0 git@github.com:yourname/Sporsho-AI-OpenMontage.git"
  exit 1
fi

cd "$(dirname "$0")/.."

echo "==> Pre-flight checks"

# 1. Confirm we are in the right repo
if [ ! -d SPORSHO ] || [ ! -f PROVENANCE.md ]; then
  echo "ERROR: not the Sporsho repository root (SPORSHO/ or PROVENANCE.md missing)."
  exit 1
fi

# 2. Confirm upstream is intact
if ! git remote get-url upstream >/dev/null 2>&1; then
  echo "WARN: no 'upstream' remote. Re-adding it."
  git remote add upstream https://github.com/calesthio/OpenMontage.git
fi
echo "    upstream: $(git remote get-url upstream)"

# 3. Confirm LICENSE is unmodified vs upstream
if git diff --quiet upstream/main -- LICENSE 2>/dev/null; then
  echo "    LICENSE: unmodified vs upstream  ✓"
else
  echo "    NOTE: LICENSE differs from upstream/main. Verify this is intentional."
fi

# 4. Block secrets
echo "==> Secret scan"
SECRETS=$(git ls-files | grep -iE '(^|/)\.env$|\.pem$|\.key$|service-account|credentials\.json' || true)
if [ -n "$SECRETS" ]; then
  echo "BLOCKED: possible secrets tracked:"; echo "$SECRETS"; exit 1
fi
# NOTE: this script excludes itself from the scan. Its own scan patterns are
# regex literals that would otherwise match themselves (an obvious false positive).
PAT='(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xoxb-[0-9A-Za-z-]{10,})'
if git grep -nIE "$PAT" -- . ':!scripts/setup-sporsho-remote.sh' ':!.gitignore' ':!docs/**' ':!PROVENANCE.md' >/dev/null 2>&1; then
  echo "BLOCKED: token-like string found:"
  git grep -nIE "$PAT" -- . ':!scripts/setup-sporsho-remote.sh' ':!.gitignore' ':!docs/**' ':!PROVENANCE.md' 2>/dev/null | sed -n '1,10p' || true
  exit 1
fi
echo "    no secrets detected  ✓"

# 5. Block oversized files (>50MB) and stray media
echo "==> Media / size scan"
BIG=$(git ls-files -z | xargs -0 -I{} sh -c \
  'test -f "{}" && s=$(stat -c%s "{}" 2>/dev/null || stat -f%z "{}" 2>/dev/null || echo 0); [ "$s" -gt 52428800 ] && echo "{} ($((s/1024/1024)) MB)"' 2>/dev/null || true)
if [ -n "$BIG" ]; then
  echo "BLOCKED: files over 50 MB (GitHub warning threshold):"; echo "$BIG"; exit 1
fi
MEDIA=$(git ls-files | grep -iE '\.(mov|mkv|avi|webm|flac|psd|tif|braw|r3d)$' || true)
if [ -n "$MEDIA" ]; then
  echo "BLOCKED: unexpected media tracked:"; echo "$MEDIA"; exit 1
fi
echo "    tracked media:"
# Capture first, then print. Piping straight into `head` would close the pipe early
# and raise SIGPIPE, which `set -o pipefail` turns into a script abort (exit 141).
MEDIA_LIST=$(git ls-files | grep -iE '\.(mp4|mp3|wav|png|jpg)$' || true)
printf '%s\n' "$MEDIA_LIST" | sed -n '1,20p' | sed 's/^/      /'
echo "    (all upstream source assets — yours never enter this repo)  ✓"

# 6. Restore full git configuration
#
# IMPORTANT: .git/config is NOT preserved by workspace snapshots (it is treated as
# a credential-bearing path). So remote URLs, the push default, identity, and the
# upstream push-lock all have to be re-applied. That is exactly what this block does.
echo "==> Configuring git"

# Identity for Sporsho commits (only if not already set)
if ! git config user.email >/dev/null 2>&1; then
  git config user.name  "Sporsho AI"
  git config user.email "sporsho-ai@users.noreply.github.com"
fi

# Ensure upstream exists and is FETCH-ONLY. A bare `git push` must never be able
# to target calesthio/OpenMontage.
if ! git remote get-url upstream >/dev/null 2>&1; then
  git remote add upstream https://github.com/calesthio/OpenMontage.git
fi
git remote set-url --push upstream DISABLED_NEVER_PUSH_TO_UPSTREAM

# origin
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

# main must NOT track upstream/main, or a bare `git push` would aim at upstream.
git branch --unset-upstream main 2>/dev/null || true

# Fail loudly rather than guess a push destination
git config push.default nothing

echo "    remotes:"
git remote -v | sed 's/^/      /'

echo
echo "==> Pushing"
echo "    Branch:   main"
echo "    Commits:  $(git rev-list --count HEAD)"
echo "    Upstream: $(git rev-parse --short upstream/main)"
echo
read -r -p "Push to origin/main? [y/N] " ans
case "$ans" in
  [yY]*) git push -u origin main ;;
  *) echo "Aborted. origin is configured; push manually when ready:"
     echo "    git push -u origin main"; exit 0 ;;
esac

echo
echo "Done."
echo
echo "Remaining manual steps:"
echo "  1. Confirm the repo is PRIVATE in GitHub settings."
echo "  2. Install the pre-push hook:  docs/sporsho/GITHUB.md § Pre-Push Hook"
echo "  3. Set the media root:         OPENMONTAGE_PROJECTS_DIR = D:\\SPORSHO AI\\projects"
echo "  4. Create D:\\SPORSHO AI\\ with projects/ and clients/ (docs/sporsho/LOCAL-MEDIA.md)"
echo "  5. Add your first client:      cp -r SPORSHO/CLIENTS/_TEMPLATE SPORSHO/CLIENTS/<slug>"
