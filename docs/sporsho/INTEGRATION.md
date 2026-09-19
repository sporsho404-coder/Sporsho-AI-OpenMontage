# INTEGRATION — Wiring Sporsho To OpenMontage

How the Sporsho layer actually connects to OpenMontage. Every seam below was verified
by reading the source at commit `08e2151`, not assumed.

**Verified vs. proposed is marked for every seam.** Nothing here claims a mechanism
that does not exist in code today.

---

## Seam Summary

| # | Seam | Status | What it wires |
|---|---|---|---|
| 1 | `OPENMONTAGE_PROJECTS_DIR` | ✅ **Verified — works today** | Project root → `D:\SPORSHO AI` |
| 2 | `styles/custom/*.yaml` | ✅ **Verified — works today** | Your look playbooks |
| 3 | `load_pipeline(..., defs_dir=)` | ✅ **Verified — works, needs code** | Custom pipeline manifests |
| 4 | Pipeline `extensions:` flags | ⚠️ **Declared, not resolved** | Would wire custom skills/playbooks |
| 5 | `config.yaml` paths | ⚠️ **Partial** | `skills_dir`, `styles_dir`, `output_dir` |
| 6 | MCP (HeyGen) | ⚠️ **Conditional** | Only if an MCP server is connected |

---

## 1. Project Root → `D:\SPORSHO AI` ✅

**This is the important one, and it works today with zero code changes.**

OpenMontage hardcodes the projects root to `<repo>/projects` but explicitly allows an
override. From `lib/paths.py`:

```python
REPO_ROOT = Path(__file__).resolve().parent.parent

# Overridable for staging/screenshots/tests. Everything — checkpoint writes,
# event attribution, the Backlot board — follows the same root.
PROJECTS_DIR = Path(os.environ.get("OPENMONTAGE_PROJECTS_DIR") or (REPO_ROOT / "projects"))
```

Upstream designed this seam on purpose. It is the officially supported way to move
the production workspace off the repo — exactly what you need.

### Linux / macOS

```bash
export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"
```

### Windows PowerShell (persistent)

```powershell
[Environment]::SetEnvironmentVariable(
  "OPENMONTAGE_PROJECTS_DIR",
  "D:\SPORSHO AI\projects",
  "User"
)
```

### Windows CMD (session)

```cmd
set OPENMONTAGE_PROJECTS_DIR=D:\SPORSHO AI\projects
```

### Why this matters

Everything follows this root:

- checkpoint writes (`lib/checkpoint.py`)
- tool event attribution
- the Backlot board watcher
- all `projects/<id>/` output paths

Set it once and **every generated asset lands on your drive, never in the repo.**
This single variable is what keeps 60 GB of client footage out of git.

> **Path with a space:** `D:\SPORSHO AI` contains a space. Always quote it in shell
> contexts. The Python side handles it fine — it is read as a single env var value.

---

## 2. Custom Style Playbooks ✅

**Works today.** `styles/playbook_loader.py` explicitly searches a `custom/`
subdirectory:

```python
CUSTOM_SUBDIR = "custom"
# Generated playbooks are written to styles/custom/ by
# lib/playbook_generator.save_playbook(); both lookups below search it as a
# fallback so those playbooks are visible to the render path.
```

Resolution order: a **preset wins** when both `styles/foo.yaml` and
`styles/custom/foo.yaml` exist. So never name a custom playbook the same as a preset.

### Your look playbooks

Put Sporsho look definitions in `styles/custom/`. They validate against
`schemas/styles/playbook.schema.json` and are picked up by `load_playbook(name)`
and `list_playbooks()` automatically.

```bash
# validate a playbook you write
python -c "from styles.playbook_loader import load_playbook; print(load_playbook('your-look')['identity']['name'])"
```

**Why `styles/custom/` and not `SPORSHO/`?** Because the loader only searches
`styles/` and `styles/custom/`. A playbook in `SPORSHO/` would be invisible to the
render path.

**Conflict risk:** upstream could add a preset with the same name as your custom
playbook. The preset would then silently win. Mitigate by prefixing your playbooks —
e.g. `sporsho-clean-corporate.yaml`, `sporsho-urgent-short.yaml`.

`styles/custom/` is **gitignored upstream** (`.gitignore` does not list it, but
`lib/playbook_generator` writes there as generated output). Verify with
`git check-ignore -v styles/custom/test.yaml` before committing. If it is ignored and
you want your playbooks versioned, add a `!styles/custom/` negation — see
§ Versioning Your Extension Points.

---

## 3. Custom Pipeline Manifests ✅ (needs a small script)

`lib/pipeline_loader.py` accepts a directory override:

```python
def load_pipeline(name: str, defs_dir: Optional[Path] = None) -> dict[str, Any]:
```

and there is a cached variant:

```python
def load_pipeline_readonly(name: str, defs_dir: Optional[Path] = None) -> dict[str, Any]:
```

So custom pipeline manifests in `SPORSHO/` are loadable — but **nothing in the CLI
calls them with `defs_dir`.** You must pass it yourself.

```python
from pathlib import Path
from lib.pipeline_loader import load_pipeline

manifest = load_pipeline("sporsho-client-short", defs_dir=Path("SPORSHO/PIPELINES"))
```

**Status:** the seam exists in the API; wiring it into your calling code is a small
task not yet done. Do not assume `python -m ...` picks up Sporsho pipelines — it does not.

**Before writing a custom pipeline**, check whether a config change to an existing
manifest gets you there. Upstream's 13 manifests already cover a lot.

---

## 4. Pipeline `extensions:` Flags ⚠️ Declared But Not Resolved

Pipeline manifests declare extension permissions:

```yaml
extensions:
  custom_scripts: true
  custom_playbooks: true
  custom_skills: true
  custom_tools: false
```

And:

```yaml
compatible_playbooks:
  recommended: [clean-professional]
  also_works: []
  custom_allowed: true
```

**These appear in YAML only.** Searching the codebase at `08e2151` finds no resolver
that reads `custom_skills` / `custom_playbooks` / `custom_scripts` / `custom_tools`.
They read as a declared contract for future behaviour, not an active mechanism.

**Practical consequence:** do not assume that adding a skill to `SPORSHO/` makes it
available to a pipeline. It does not, today. Point agents at Sporsho files
explicitly in your prompt or config instead.

This is worth watching on upstream updates — if a resolver lands, this becomes a
real seam.

---

## 5. `config.yaml` Paths ⚠️ Partial

```yaml
paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

| Key | Sporsho relevance |
|---|---|
| `styles_dir` | **Potential seam** — could point at a Sporsho styles dir. The loader's `styles_dir` parameter is used by `styles/playbook_loader.py`, so this is likely workable. Verify before relying on it. |
| `output_dir` | `output/` is **gitignored**. Production outputs belong under `projects/` (which respects `OPENMONTAGE_PROJECTS_DIR`), not here. |
| `skills_dir` | Sporsho skills are *instructions*, not OpenMontage skills. Don't point this at `SPORSHO/` — agents read Sporsho files by explicit reference. |
| `pipeline_dir` | Where `init_project` writes checkpoints. Follows the project root, not this key. |
| `library_dir` | Music library. |

Also set here: `budget.mode`, `budget.total_usd`, `checkpoint.policy`, and default
output format/codec/resolution/fps/crf. Set your house defaults here — this file is
**upstream-owned**, so if you change it, expect merge conflicts on every upstream
update. Prefer documenting desired values in `SPORSHO/` and changing this file only
when you must.

---

## 6. MCP Integrations ⚠️ Conditional

MCP is used **only for HeyGen**, and only as a *preference* over direct API calls.
From `.agents/skills/text-to-speech/SKILL.md`:

> *"If HeyGen MCP tools are available (`mcp__heygen__*`), **prefer them** over direct
> HTTP API calls."*

`.agents/skills/video-translate/SKILL.md` and `text-to-speech/SKILL.md` declare
`allowed-tools: mcp__heygen__*`. `heygen` references document MCP equivalents
(`mcp__heygen__get_video`, `mcp__heygen__generate_video_agent`) with direct-API
fallbacks.

**There is no general MCP framework here.** MCP is a HeyGen-specific optimization.
If no HeyGen MCP server is connected, the direct API path is used — nothing breaks.

**Sporsho implication:** don't plan MCP integration for other providers. There is
no seam for it. If you want MCP for e.g. a DAM or an asset manager, that is a
genuine feature to build, not a configuration change.

---

## Versioning Your Extension Points

Your custom assets live in upstream-owned directories (`styles/custom/`). Make sure
they're tracked:

```bash
git check-ignore -v styles/custom/sporsho-clean-corporate.yaml
```

If a path is ignored and you want it versioned, add a negation to `.gitignore`:

```gitignore
!styles/custom/
!styles/custom/*.yaml
```

Negations must come **after** the ignoring pattern, and git will not re-include files
inside an excluded *directory* — so exclude contents (`styles/custom/*`) rather than
the directory itself if you hit that. Test with `git check-ignore` after every change.

**Alternative that avoids the conflict entirely:** keep the *source of truth* for
your playbooks in `SPORSHO/PROMPTS/` or `SPORSHO/EDITING-RULES/`, and treat
`styles/custom/` as generated output you copy in. Then a `git merge` can never
conflict on your look definitions.

---

## The AGPL-3.0 Question ⚠️ Read This

**OpenMontage is licensed AGPL-3.0**, not MIT or Apache. The full text is in
`LICENSE` (661 lines). This has real consequences.

### What is fine

- ✅ A **private** repository. AGPL obligations trigger on distribution and on
  offering the software over a network. A private repo does neither. No obligation is
  triggered.
- ✅ Using it internally to produce client videos. **The videos you make are yours.**
  AGPL covers the software, not the output.
- ✅ Modifying it privately for your own use.
- ✅ Keeping the licence and copyright notices intact — which this repo does.

### What to watch

- ⚠️ **Making this repository public** = distribution. You would need to provide
  complete corresponding source under AGPL-3.0 to anyone who receives it.
- ⚠️ **AGPL §13, the network clause.** If you ever *host* a modified OpenMontage so
  that users interact with it over a network, you must offer those users the
  corresponding source of your modified version. **This includes your modifications.**
  Serving an editing service to clients from a modified OpenMontage could trigger this.
- ⚠️ **Combining with proprietary code.** Careful about linking AGPL code into a
  closed-source product you distribute.

### Practical guidance for Sporsho

1. **Keep the repository private.** This is the current plan and it is correct.
2. **Keep `LICENSE` and attribution intact.** Done — the file is unmodified.
3. **Keep Sporsho in a separate directory.** This also happens to be good AGPL
   hygiene: it makes the boundary between upstream and your work legible.
4. **Get legal advice before commercialising** any hosted service built on this.
   This document is not legal advice.

### Attribution

The repository preserves:

- `LICENSE` — the complete original AGPL-3.0 text, unmodified (661 lines)
- The full upstream git history (449 commits), preserving every author's authorship
- The `upstream` remote pointing at `calesthio/OpenMontage`
- Upstream's `README.md`, `CONTRIBUTING.md`, `CODEOWNERS`, and all notices

`PROVENANCE.md` at the repo root records the import, the exact commit, and the date.

**This repository is a derivative work. OpenMontage is the work of calesthio and its
contributors. Sporsho AI is the customization layer on top.**

---

## Update Procedure

```bash
git fetch upstream
git merge upstream/main
```

Conflicts can only occur in upstream-owned files. `SPORSHO/` is not in upstream's
tree, so it cannot conflict.

**Exception:** if you are tracking custom playbooks in `styles/custom/` and upstream
adds a preset of the same name, you get a silent behaviour change, not a merge
conflict — the preset wins. Prefix your playbook names to avoid this.

After any merge, re-verify:

- [ ] `SPORSHO/` is intact
- [ ] `LICENSE` is still unmodified
- [ ] Any `styles/custom/` playbooks still load and aren't shadowed by new presets
- [ ] `OPENMONTAGE_PROJECTS_DIR` still respected (re-read `lib/paths.py`)
- [ ] If `lib/pipeline_loader.py` changed, recheck the `defs_dir` seam
- [ ] If a new resolver for `extensions:` landed, revisit § 4
- [ ] `OPENMONTAGE_VERSION` in `PROVENANCE.md` updated

Never `git rebase` or force-push `main`. It would break the connection to upstream
history and make future merges impossible.
