# GITHUB — Repository Operations

How this repository relates to GitHub and to upstream OpenMontage.

---

## Repository Facts

| | |
|---|---|
| **Name** | `Sporsho-AI-OpenMontage` |
| **Visibility** | **Private** |
| **Base** | `calesthio/OpenMontage` @ `08e2151fa02de28a5d6a312b3d575692bf147ad7` |
| **Upstream history** | Preserved — 449 commits |
| **Licence** | AGPL-3.0 (inherited, unmodified) |
| **Remotes** | `origin` → your repo · `upstream` → `calesthio/OpenMontage` |

> **This is not a GitHub fork.** It is a fresh, private repository with upstream
> history imported and an `upstream` remote configured. That choice is deliberate:
> a fork of an AGPL project is public, and forks cannot be made private. See
> `INTEGRATION.md` § The AGPL-3.0 Question.

---

## Remote Setup

```bash
git remote -v
# origin    git@github.com:<you>/Sporsho-AI-OpenMontage.git
# upstream  https://github.com/calesthio/OpenMontage.git
```

`upstream` is **fetch-only.** Its push URL is deliberately set to a dead string
(`DISABLED_NEVER_PUSH_TO_UPSTREAM`) so a mistaken push cannot reach
`calesthio/OpenMontage`. You do not own that repository, and pushing there would be an
unrelated change to someone else's project.

Additionally, `push.default` is set to `nothing`, so a bare `git push` fails loudly
instead of guessing a destination.

### ⚠️ `.git/config` Is Not Preserved

If this repository is carried between environments (clones, workspace snapshots,
machines), **`.git/config` may not travel with it** — it is commonly treated as a
credential-bearing path and excluded. That means remote URLs, the push lock, the push
default, and your commit identity can all be lost.

`scripts/setup-sporsho-remote.sh` restores every one of those in a single run. Run it
first whenever `git remote -v` looks wrong or empty.

Verify the guards are in place:

```bash
git remote -v
# upstream <url> (fetch)
# upstream DISABLED_NEVER_PUSH_TO_UPSTREAM (push)   <-- must look like this

git config push.default          # must print: nothing
git branch -vv                   # local main must NOT show [upstream/main]
```

---

## Day-To-Day

```bash
git status
git add SPORSHO/                           # your layer
git commit -m "rules: ..."                 # scoped message
git push origin main
```

### Commit Message Convention

Prefix with the area, so history stays readable:

| Prefix | For |
|---|---|
| `rules:` | `SPORSHO/EDITING-RULES/` |
| `client:` | `SPORSHO/CLIENTS/` |
| `workflow:` | `SPORSHO/WORKFLOWS/` |
| `prompts:` | `SPORSHO/PROMPTS/` |
| `memory:` | `SPORSHO/MEMORY/` |
| `qc:` | `SPORSHO/QC/` |
| `brain:` | `SPORSHO/BRAIN/` |
| `refs:` | `SPORSHO/REFERENCES/` |
| `docs:` | repository-level documentation |
| `chore:` | housekeeping |

Examples:
```
rules: set default min shot hold to 0.8s
client: add acme-corp, register=steady
memory: lesson from 2026-09-20 shorts batch
```

---

## Updating From Upstream

```bash
git fetch upstream
git diff upstream/main --stat        # see what changed before merging
git merge upstream/main
```

**Before merging**, check whether the seams in `docs/sporsho/INTEGRATION.md` changed:

```bash
git diff upstream/main -- lib/paths.py lib/pipeline_loader.py styles/playbook_loader.py
```

If any of those moved, the Sporsho layer's assumptions may need revisiting. Update
`PROVENANCE.md` with the new commit after merging.

**Never** `git rebase` or force-push `main`. It severs the connection to upstream
history and makes future merges impossible.

---

## Never Commit

- `.env`, API keys, tokens, service-account JSON
- Media: `.mp4 .mov .mkv .wav .mp3 .psd` and friends
- `projects/`, `output/`, `pipeline/`, `corpus/`, `music_library/`
- `node_modules/`, build outputs, caches
- Client footage, in any form

---

## Pre-Push Hook

Automate the safety checks so you cannot forget. Create `.git/hooks/pre-push`:

```bash
#!/usr/bin/env bash
set -e
fail=0

# 1. Block files over 50 MB
while read -r f; do
  [ -f "$f" ] || continue
  sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
  if [ "$sz" -gt 52428800 ]; then
    echo "BLOCKED: $f is $((sz/1024/1024)) MB (>50 MB GitHub warning threshold)"
    fail=1
  fi
done < <(git ls-files)

# 2. Block media extensions
if git ls-files | grep -qiE '\.(mp4|mov|mkv|avi|wav|flac|psd|tif)$'; then
  echo "BLOCKED: media files are tracked"
  git ls-files | grep -iE '\.(mp4|mov|mkv|avi|wav|flac|psd|tif)$'
  fail=1
fi

# 3. Block secrets
if git ls-files | grep -qiE '(^|/)\.env$|credentials|service-account|\.pem$'; then
  echo "BLOCKED: possible secrets tracked"
  fail=1
fi

# 4. Ad-hoc secret scan
if git grep -nIE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' -- . >/dev/null 2>&1; then
  echo "BLOCKED: token-like string found in tracked files"
  git grep -nIE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' -- . | head
  fail=1
fi

[ "$fail" -eq 0 ] || { echo "Push aborted."; exit 1; }
echo "Pre-push checks passed."
```

```bash
chmod +x .git/hooks/pre-push
```

Hooks are local and not versioned by git. Commit the script elsewhere
(e.g. `scripts/pre-push-hook.sh`) and symlink it, so a fresh clone can reinstall it.

---

## Visibility

**Keep it private.** Changing visibility is gated:

- Public = distribution under AGPL-3.0, triggering full source-provision obligations
- Public also exposes your client profiles and your competitive editing rules

Changing visibility requires explicit approval per
`SPORSHO/BRAIN/OPERATING-PRINCIPLES.md` §9.

If you ever genuinely need an upstream contribution, send the patch **to upstream**
as a pull request — do not make this repository public to do it.
