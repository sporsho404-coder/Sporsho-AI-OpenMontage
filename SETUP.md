# SETUP — Finish The Installation

The repository is **built, committed, and verified**. Three steps remain, all of which
need your credentials or your machine.

Total time: about 10 minutes.

---

## Step 0 — Why You're Doing This Manually

This environment has **no access to your GitHub account**. Verified:

```
GET https://api.github.com/user  →  401 Unauthorized
```

No token, no `gh` CLI, no stored credentials. So the repository was prepared locally
with everything committed and verified, and the push is yours to run.

That is also why **nothing on your GitHub account was touched** — no repositories
created, modified, or deleted. There was no access to do so.

---

## Step 1 — Create The Private Repository

Go to **https://github.com/new**

| Field | Value |
|---|---|
| Repository name | `Sporsho-AI-OpenMontage` |
| Description | Sporsho AI video-editing brain — OpenMontage core + customization layer |
| Visibility | **Private** ← required, see the AGPL note below |
| Initialize with README | ❌ **off** |
| Add .gitignore | ❌ **None** |
| Choose a license | ❌ **None** |

**Do not initialise with anything.** This repository already has 450 commits of
history. Initialising creates a conflicting commit and you'd have to force-push.

> **Why Private is required:** OpenMontage is **AGPL-3.0**. A public repository is
> distribution, which triggers source-provision obligations. A private one does not.
> You can change this later, but it is a gated decision — see
> `docs/sporsho/INTEGRATION.md` § The AGPL-3.0 Question.

---

## Step 2 — Configure And Push

From the repository directory:

```bash
./scripts/setup-sporsho-remote.sh git@github.com:YOUR_USERNAME/Sporsho-AI-OpenMontage.git
```

Replace `YOUR_USERNAME`. Use the HTTPS form if you don't have SSH keys:

```bash
./scripts/setup-sporsho-remote.sh https://github.com/YOUR_USERNAME/Sporsho-AI-OpenMontage.git
```

The script will:

1. Verify `upstream` is intact
2. Confirm `LICENSE` is unmodified vs. upstream
3. Scan for secrets (`sk-`, `ghp_`, `AKIA`, `.env`, `.pem`, service accounts)
4. Scan for oversized files (>50 MB) and stray media
5. Configure `origin`, lock `upstream` to fetch-only, unset bad branch tracking
6. Show you a summary and **ask before pushing**

Review the output, then confirm.

### Why the script matters

`.git/config` is frequently **not preserved** when a repository moves between machines
or snapshots — it is treated as credential-bearing. Remote URLs, the push lock, the
push default, and your commit identity can all be lost. This script restores all of it.

---

## Step 3 — Verify

```bash
git log --oneline -3        # your Sporsho commit on top of upstream
git remote -v               # upstream push URL must read DISABLED_...

# Local checks
git status --porcelain      # must be empty
```

Then confirm on GitHub:

- [ ] Repository exists at `github.com/YOUR_USERNAME/Sporsho-AI-OpenMontage`
- [ ] **Visibility badge reads "Private"**
- [ ] `LICENSE` is present and is AGPL-3.0 (661 lines)
- [ ] `SPORSHO/` folder exists with 9 subfolders
- [ ] `SPORSHO.md` renders as documentation
- [ ] Commit count is ~450 (upstream history preserved + 1 Sporsho commit)
- [ ] No `.env`, no footage, no renders anywhere in the tree

---

## Step 4 — Optional, Recommended

### 4a. Install the pre-push hook

`.git/hooks/pre-push` blocks large files, media, and secrets before they ever leave
your machine. The full script is in `docs/sporsho/GITHUB.md` § Pre-Push Hook.

This is the highest-value five minutes in this setup. A 20 GB render committed once is
permanent — git history cannot be shrunk.

### 4b. Point OpenMontage at your drive

**This is the step that keeps media out of git**, verified in `lib/paths.py`:

```powershell
# Windows — persistent
[Environment]::SetEnvironmentVariable(
  "OPENMONTAGE_PROJECTS_DIR", "D:\SPORSHO AI\projects", "User")
```

```bash
# Linux / macOS / WSL
export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"
```

Verify:

```bash
python -c "from lib.paths import PROJECTS_DIR; print(PROJECTS_DIR)"
# must print your drive path, NOT <repo>/projects
```

### 4c. Create the drive layout

See `docs/sporsho/LOCAL-MEDIA.md` for the full tree. Minimum:

```
D:\SPORSHO AI\
├── projects\      ← OPENMONTAGE_PROJECTS_DIR points here
├── clients\
├── references\
├── library\{music,sfx,broll,fonts,luts}\
├── exports\
├── cache\
└── .env           ← your API keys. NEVER commit this.
```

### 4d. Add your first client

```bash
cp -r SPORSHO/CLIENTS/_TEMPLATE SPORSHO/CLIENTS/your-first-client
```

Then fill in `PROFILE.md` and `EDITING-RULES.md`. Start with just those two —
`BRAND.md`, `DELIVERY.md`, and `REVISION-LOG.md` fill in as you work.

---

## Verifying The Install Worked

```bash
# 1. Sporsho layer intact?
ls SPORSHO/BRAIN SPORSHO/CLIENTS SPORSHO/MEMORY SPORSHO/QC

# 2. Licence preserved?
git diff upstream/main -- LICENSE          # must be empty

# 3. Upstream still reachable for updates?
git fetch upstream && git merge upstream/main --dry-run

# 4. Media root wired?
python -c "from lib.paths import PROJECTS_DIR; print(PROJECTS_DIR)"

# 5. No secrets, no media?
git ls-files | grep -iE '(^|/)\.env$|\.pem$' || echo "clean"
```

---

## If Something Goes Wrong

| Symptom | Cause | Fix |
|---|---|---|
| `fatal: No configured push destination` | `push.default` is `nothing` — this is intentional | Name the remote: `git push -u origin main` |
| `error: remote origin already exists` | Re-running the script | Harmless; it updates the URL instead |
| Push rejected, non-fast-forward | Repo was initialised with a README | Delete the GitHub repo, recreate empty, retry |
| `OPENMONTAGE_PROJECTS_DIR` ignored | Set in a terminal you didn't restart | Restart the shell, or set it in the launching environment |
| `git fetch upstream` fails | Remote removed | `git remote add upstream https://github.com/calesthio/OpenMontage.git` |
| Merge conflict inside `SPORSHO/` | Something edited an upstream file to hold Sporsho knowledge | Stop and fix — see `SPORSHO/INTEGRATIONS/UPSTREAM.md` |

---

## After Setup

Read, in this order:

1. [`SPORSHO.md`](SPORSHO.md) — the architecture
2. [`SPORSHO/BRAIN/OPERATING-PRINCIPLES.md`](SPORSHO/BRAIN/OPERATING-PRINCIPLES.md) — how it thinks
3. [`docs/sporsho/CAPABILITY-MAP.md`](docs/sporsho/CAPABILITY-MAP.md) — what actually exists
4. [`docs/sporsho/INTEGRATION.md`](docs/sporsho/INTEGRATION.md) — the wiring
5. [`SPORSHO/WORKFLOWS/TALKING-HEAD-TO-SHORT.md`](SPORSHO/WORKFLOWS/TALKING-HEAD-TO-SHORT.md) — your first real job

Then run one real project. After it ships, write the memory entry —
that's what turns this from a repository into a brain.
