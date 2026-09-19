#!/usr/bin/env bash
# =============================================================================
# push-with-token.sh — one-shot push using a GitHub Personal Access Token
#
# DESIGNED TO MINIMISE TOKEN EXPOSURE:
#   • Reads the token from a FILE (never an argument — arguments land in ps/history)
#   • Uses a throwaway credential store inside this script only
#   • Never writes the token into .git/config, and never echoes it
#   • Wipes the credential store on exit, success or failure
#
# RECOMMENDED TOKEN SCOPE (fine-grained PAT, https://github.com/settings/tokens):
#   Repository access : Only select repositories -> Sporsho-AI-OpenMontage
#   Permissions       : Contents = Read and write   (that is all that is needed)
#   Expiration        : 7 days  (then revoke it)
#
# Usage:
#   ./scripts/push-with-token.sh /path/to/token-file
#
# The token file should contain ONLY the token, nothing else.
# =============================================================================
set -uo pipefail

cd "$(dirname "$0")/.."

TOKEN_FILE="${1:-}"
ORIGIN_URL="https://github.com/sporsho404-coder/Sporsho-AI-OpenMontage.git"

if [ -z "$TOKEN_FILE" ]; then
  echo "Usage: $0 /path/to/token-file"
  echo
  echo "The file must contain only the token, e.g.:"
  echo "  github_pat_11ABC...xyz"
  exit 1
fi

if [ ! -f "$TOKEN_FILE" ]; then
  echo "ERROR: token file not found: $TOKEN_FILE"
  exit 1
fi

TOKEN=$(tr -d ' \t\r\n' < "$TOKEN_FILE")
if [ -z "$TOKEN" ]; then
  echo "ERROR: token file is empty."
  exit 1
fi
if [ "${#TOKEN}" -lt 20 ]; then
  echo "ERROR: token looks too short (${#TOKEN} chars). Wrong file?"
  exit 1
fi
echo "Token loaded: ${#TOKEN} chars, prefix ${TOKEN:0:11}..."

# Throwaway credential store, removed on exit no matter what happens.
CRED_DIR=$(mktemp -d)
CRED_FILE="$CRED_DIR/creds"
cleanup() {
  rm -rf "$CRED_DIR"
  # Remove the token file the caller handed us
  rm -f "$TOKEN_FILE"
  echo
  echo "Cleaned up: temporary credential store and token file removed."
}
trap cleanup EXIT INT TERM

printf 'https://sporsho404-coder:%s@github.com\n' "$TOKEN" > "$CRED_FILE"
chmod 600 "$CRED_FILE"

echo
echo "==> Verifying token before pushing"
# IMPORTANT: check the EXIT CODE, not whether output is empty. On failure git
# prints its error text to the captured stream, so a non-empty check would
# wrongly report success for a rejected token.
PROBE=$(GIT_TERMINAL_PROMPT=0 git -c credential.helper="store --file=$CRED_FILE" \
        ls-remote "$ORIGIN_URL" HEAD 2>&1)
PROBE_RC=$?
if [ "$PROBE_RC" -ne 0 ]; then
  echo "ERROR: authentication failed — token rejected or lacks access."
  echo "$PROBE" | grep -viE 'github_pat|[0-9a-f]{40}' | sed 's/^/  /' | head -5
  echo
  echo "Check: token is not expired, is scoped to this repo, and has Contents: Read and write."
  exit 1
fi
echo "    authenticated OK  ✓"
if [ -z "$PROBE" ]; then
  echo "    remote HEAD: (none) — repo has no commits yet, which is expected"
else
  echo "    remote HEAD: $(echo "$PROBE" | awk '{print $1}' | cut -c1-12)"
fi

echo
echo "==> Pushing (no force, no re-init, existing history only)"
if GIT_TERMINAL_PROMPT=0 git -c credential.helper="store --file=$CRED_FILE" \
     push -u origin main; then
  PUSH_OK=1
else
  PUSH_OK=0
fi

echo
if [ "$PUSH_OK" -eq 1 ]; then
  echo "=============================================================="
  echo " PUSH SUCCEEDED"
  echo "=============================================================="
  git -c credential.helper="store --file=$CRED_FILE" fetch origin --quiet 2>/dev/null || true
  echo "  origin/main : $(git rev-parse --short origin/main 2>/dev/null || echo '?')"
  echo "  local  main : $(git rev-parse --short main)"
  echo "  commits     : $(git rev-list --count main)"
  echo "  repo        : https://github.com/sporsho404-coder/Sporsho-AI-OpenMontage"
  echo
  echo "  Verify in the GitHub UI:"
  echo "    [ ] Visibility still reads PRIVATE"
  echo "    [ ] Commit count matches $(git rev-list --count main)"
  echo "    [ ] No .env, footage, or renders in the file tree"
  echo
  echo "  THEN REVOKE THE TOKEN:"
  echo "    https://github.com/settings/tokens"
  echo
  echo "  Re-run full verification any time with: ./scripts/push-and-verify.sh"
else
  echo "=============================================================="
  echo " PUSH FAILED"
  echo "=============================================================="
  echo "  If the error mentions non-fast-forward, the GitHub repo was"
  echo "  initialised with a README. Delete it and recreate EMPTY."
  exit 1
fi
