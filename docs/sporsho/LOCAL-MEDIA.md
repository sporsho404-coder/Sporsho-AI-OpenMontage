# LOCAL MEDIA — `D:\SPORSHO AI`

Heavy assets live on your drive. Never in git. Never uploaded.

---

## Why This Is Absolute

Git repositories cannot be shrunk. A 40 GB client shoot committed once stays in the
history forever — even if you delete the file in a later commit. The only remedy is
rewriting history, which invalidates every clone and breaks your link to upstream.

Changing your mind later is not an option. So: **no media in git, ever.**

GitHub also hard-fails pushes above 100 MB per file and warns above 50 MB.

---

## The Split

| | GitHub repo | `D:\SPORSHO AI` |
|---|---|---|
| Code, skills, rules | ✅ | |
| Client profiles, editing rules | ✅ | |
| Prompts, workflows | ✅ | |
| Reference **analysis notes** (markdown) | ✅ | |
| Memory, lessons | ✅ | |
| Lightweight metadata (JSON manifests) | ✅ | |
| Client footage | | ✅ |
| Reference **video files** | | ✅ |
| Renders and exports | | ✅ |
| Music and SFX libraries | | ✅ |
| Generated assets (images, clips) | | ✅ |
| API keys and `.env` | | ✅ (**never** GitHub) |

---

## Recommended Layout

```
D:\SPORSHO AI\
├── projects\                 ← OPENMONTAGE_PROJECTS_DIR points HERE
│   └── <project-id>\         ← OpenMontage writes its canonical layout here
│       ├── artifacts\        ← JSON artifacts per stage
│       ├── assets\
│       │   ├── images\  video\  audio\  music\
│       │   └── subtitles.srt
│       ├── renders\
│       │   └── final.mp4     ← the deliverable
│       └── project.json      ← the marker the Backlot board reads
│
├── clients\
│   └── <client-slug>\
│       ├── footage\          ← raw source
│       ├── references\       ← videos the client sent
│       ├── deliverables\     ← shipped versions, by date
│       ├── brand\            ← logos, fonts, brand assets
│       └── archive\          ← superseded cuts
│
├── references\               ← YOUR reference library
│   └── <slug>\               ← matches SPORSHO/REFERENCES/<slug>/
│       └── source.mp4
│
├── library\
│   ├── music\
│   ├── sfx\
│   ├── broll\
│   ├── fonts\
│   └── luts\
│
├── exports\                  ← final, client-ready
├── cache\                    ← regenerable; safe to delete
└── .env                      ← API KEYS. NEVER COMMIT. NEVER SHARE.
```

`projects\` matches OpenMontage's own project-directory convention exactly
(`AGENT_GUIDE.md` → "Project Directory Convention"). That matters — the Backlot board
and every tool's `output_path` expect that shape.

---

## Wiring It Up

```bash
# Linux / macOS (WSL)
export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"
```

```powershell
# Windows — persistent, user-level
[Environment]::SetEnvironmentVariable("OPENMONTAGE_PROJECTS_DIR", "D:\SPORSHO AI\projects", "User")
```

Verified against `lib/paths.py`. See `INTEGRATION.md` § 1.

---

## Secrets

**`.env` must never be committed.** It holds keys for 30+ providers
(FAL, OpenAI, ElevenLabs, Suno, HeyGen, Runway, Azure, and more — see `.env.example`).

Upstream's `.gitignore` already blocks `.env`, `.env.local`, `*.env`, `gcp-*.json`,
`*-service-account.json`. This repo adds further layers. Verify before pushing:

```bash
git check-ignore -v .env          # must output a rule
git ls-files | grep -i -E '\.env|secret|credential|token'   # must be empty
```

**If a key is ever committed, treat it as compromised.** Rotate it. Deleting the commit
is not enough — it stays in history and in any clone.

---

## Rules For Agents

1. Never write media into the repository. Use `projects/<id>/` paths, which resolve to
   the drive via `OPENMONTAGE_PROJECTS_DIR`.
2. Always pass an explicit `output_path` under `projects/<project-id>/`.
   Upstream: assets written to the repo root or a temp dir are **invisible to the user's
   board** and violate the workspace contract.
3. Never `git add` a media file. If `git status` shows one, stop and diagnose.
4. Never upload client footage anywhere off the local machine without explicit approval.
5. `cache\` is disposable. `deliverables\` is not.

---

## Pre-Push Safety Check

```bash
# Files over 10 MB that are staged or tracked
git ls-files -z | xargs -0 du -h 2>/dev/null | sort -rh | head -20

# Any media anywhere in the tracked set
git ls-files | grep -i -E '\.(mp4|mov|mkv|avi|wav|mp3|flac|psd|tif|png|jpg|raw)$'

# Anything over 50 MB (GitHub's warning threshold)
git ls-files -z | xargs -0 -I{} sh -c 'test -f "{}" && test $(stat -c%s "{}" 2>/dev/null || stat -f%z "{}") -gt 52428800 && echo "{}"'
```

Run these **before every push**. A `.git/hooks/pre-push` hook can automate it — see
the repository `scripts/` notes.
