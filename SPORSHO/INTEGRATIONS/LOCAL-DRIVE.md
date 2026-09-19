# Integration — LOCAL DRIVE (`D:\SPORSHO AI`)

Wiring the drive, per platform.

**Full detail:** [`../../docs/sporsho/LOCAL-MEDIA.md`](../../docs/sporsho/LOCAL-MEDIA.md)

---

## The One Variable

```bash
OPENMONTAGE_PROJECTS_DIR=D:\SPORSHO AI\projects
```

Verified in `lib/paths.py`. Everything follows it: checkpoints, event attribution,
the Backlot board, all project output paths.

---

## Per Platform

### Windows — PowerShell (persistent, recommended)

```powershell
[Environment]::SetEnvironmentVariable(
  "OPENMONTAGE_PROJECTS_DIR", "D:\SPORSHO AI\projects", "User")
```

Restart the terminal. Verify:

```powershell
[Environment]::GetEnvironmentVariable("OPENMONTAGE_PROJECTS_DIR", "User")
```

### Windows — CMD (current session)

```cmd
set OPENMONTAGE_PROJECTS_DIR=D:\SPORSHO AI\projects
```

### WSL

```bash
# If the repo lives in WSL and the drive is mounted at /mnt/d
echo 'export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"' >> ~/.bashrc
source ~/.bashrc
```

> **WSL path caveat:** reading and writing `/mnt/d` from WSL is markedly slower than
> native NTFS access for large media. If video work feels sluggish, run OpenMontage
> natively on Windows and keep WSL for lightweight work only.

### Linux / macOS

```bash
echo 'export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"' >> ~/.bashrc
```

(Substitute the real mount point if the drive is elsewhere.)

---

## Verify It Took Effect

```bash
python -c "from lib.paths import PROJECTS_DIR; print(PROJECTS_DIR)"
```

The output must be your drive path, **not** `<repo>/projects`.
If it shows the repo path, the variable is not visible to that process.

Common causes:
1. Set in a terminal that was not restarted
2. Set in one shell but the process ran in another (e.g. a GUI-launched agent)
3. A typo in the variable name — it is `OPENMONTAGE_PROJECTS_DIR`, exactly
4. WSL vs Windows environment separation — they are **not** shared by default

---

## Directory Layout

See `docs/sporsho/LOCAL-MEDIA.md` for the full recommended tree. The critical part:

```
D:\SPORSHO AI\
└── projects\
    └── <project-id>\
        ├── artifacts\
        ├── assets\{images,video,audio,music}\
        ├── renders\final.mp4
        └── project.json
```

This mirrors OpenMontage's own project-directory convention exactly, because the
Backlot board and every tool's `output_path` expect that shape.

---

## Rules

1. **`projects\` is regenerable.** Everything in it can be rebuilt. Don't back it up
   religiously; do back up `clients\<slug>\deliverables\`.
2. **`cache\` is disposable.** Delete it freely.
3. **`.env` lives on the drive, never in the repo.**
4. **Never symlink `projects\` into the repo.** A symlink is a one-commit-away
   accident that puts 60 GB into git history permanently.
5. **Agents must pass explicit `output_path` values** under `projects/<project-id>/`.
   Upstream: assets written to the repo root or a temp dir are invisible to the
   board and violate the workspace contract.
