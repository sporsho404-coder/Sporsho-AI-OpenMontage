# Integration — GITHUB

Points to the repository operations doc.

**Full detail:** [`../../docs/sporsho/GITHUB.md`](../../docs/sporsho/GITHUB.md)

---

## The Short Version

```
origin    → your private repo (Sporsho-AI-OpenMontage)
upstream  → https://github.com/calesthio/OpenMontage (fetch only, never push)
```

```bash
# daily
git add SPORSHO/ && git commit -m "rules: ..." && git push origin main

# monthly
git fetch upstream && git merge upstream/main
```

## ⚠️ Run This First In A Fresh Environment

`.git/config` is often **not preserved** when a repository moves between machines or
snapshots (it is treated as credential-bearing). Remote URLs, the push lock, the push
default, and your commit identity can all be lost.

```bash
./scripts/setup-sporsho-remote.sh git@github.com:YOUR_USERNAME/Sporsho-AI-OpenMontage.git
```

It restores everything and runs secret/size/media pre-flight checks before pushing.

## Rules

1. **Never push to `upstream`.** Its push URL is deliberately disabled. You do not own
   it. Pushing there would be an unrelated change to someone else's project.
2. **`push.default` is `nothing`** — a bare `git push` fails loudly rather than guessing.
   Always name the remote: `git push origin main`.
3. **Never force-push or rebase `main`.** It severs the link to upstream history.
4. **Keep it private.** AGPL-3.0 — public means distribution obligations.
   See `docs/sporsho/INTEGRATION.md` § The AGPL-3.0 Question.
5. **Install the pre-push hook.** `docs/sporsho/GITHUB.md` has a ready-to-use script
   that blocks large files, media, and secrets.

## Verify The Guards

```bash
git remote -v                  # upstream push URL must be DISABLED_...
git config push.default        # must print: nothing
git branch -vv                 # main must NOT show [upstream/main]
```
