# Provenance

Record of what this repository is built from, and what has been changed.

---

## Upstream Source

| | |
|---|---|
| **Project** | OpenMontage |
| **Repository** | https://github.com/calesthio/OpenMontage |
| **Licence** | **GNU Affero General Public License v3.0 (AGPL-3.0)** |
| **Licence file** | [`LICENSE`](LICENSE) — 661 lines, **unmodified** |
| **Imported commit** | `08e2151fa02de28a5d6a312b3d575692bf147ad7` |
| **Commit date** | 2026-09-05 |
| **Commit subject** | `docs: add Objects in Overdrive video showcase` |
| **History preserved** | Yes — 449 commits |
| **Import date** | 2026-09-20 |

```
OPENMONTAGE_VERSION = 08e2151fa02de28a5d6a312b3d575692bf147ad7
```

## This Repository

| | |
|---|---|
| **Name** | Sporsho-AI-OpenMontage |
| **Visibility** | Private |
| **Purpose** | Long-term AI video-editing brain |
| **Relationship to upstream** | Derivative work — upstream core plus a separate customization layer |

**This repository is a derivative work of OpenMontage by calesthio and its
contributors.** The Sporsho layer (`SPORSHO/`, `docs/sporsho/`) is original work.
The OpenMontage core is not.

---

## Attribution Preserved

Verified intact at import:

- ✅ `LICENSE` — complete AGPL-3.0 text, byte-identical to upstream
- ✅ Full upstream git history (449 commits) — every contributor's authorship preserved
- ✅ Upstream `README.md`, `README_zh-CN.md`, `CONTRIBUTING.md`, `CODEOWNERS`
- ✅ All source headers and notices
- ✅ `upstream` remote configured, pointing at `calesthio/OpenMontage`
- ✅ No upstream file renamed, moved, or hidden

Nothing was removed, hidden, or rebranded. OpenMontage remains recognisable as
OpenMontage.

---

## Local Modifications

**None.** The Sporsho layer is purely additive.

| Upstream path | Modified? |
|---|---|
| `LICENSE` | No |
| `README.md` | No |
| `AGENT_GUIDE.md` | No |
| `config.yaml` | No |
| `pipeline_defs/` | No |
| `tools/`, `lib/`, `skills/`, `styles/`, `.agents/`, `schemas/` | No |

The only file touched at the repository root is `.gitignore`, which received
**additive** Sporsho rules (media and secret guards). No upstream rule was removed
or weakened. See the commit for the exact diff.

**Zero local patches to upstream files** is the standing policy. See
`SPORSHO/INTEGRATIONS/UPSTREAM.md` for why this matters and what to do if a patch
ever becomes unavoidable.

---

## What Was Imported

Full upstream tree at `08e2151`, including:

| Path | Contents |
|---|---|
| `AGENT_GUIDE.md` | 48 KB — the authoritative agent contract |
| `PROJECT_CONTEXT.md`, `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `CURSOR.md`, `COPILOT.md` | Agent context files |
| `PROMPT_GALLERY.md` | Generic prompt library |
| `pipeline_defs/` | 13 pipeline manifests |
| `tools/` | ~100 tools across 12 families |
| `skills/` | ~110 skills — core, creative, meta, pipelines |
| `.agents/skills/` | ~85 Layer-3 vendor skills |
| `styles/` | 5 look playbooks + loader |
| `schemas/` | Artifact, checkpoint, pipeline, style, tool schemas |
| `lib/` | 20 support modules |
| `docs/` | Architecture, providers, guides |
| `backlot/` | Production board UI |
| `remotion-composer/` | Remotion composition runtime |
| `ink-theater/` | Hand-drawn animation runtime |
| `tests/` | Test suite |
| `.github/` | CI, issue templates, prompts |

**Not modified, not trimmed, not reorganised.**

### Note on upstream media assets

Upstream tracks a small number of media files that are **part of its source tree
and its documentation** — including `assets/signal-from-tomorrow-demo.mp4` (20 MB)
and HyperFrames example clips (16 MB). These are retained deliberately:

- They are upstream-tracked source files, not generated output
- Removing them would modify the OpenMontage core and break skill examples
- The largest is 20 MB — well under GitHub's 50 MB warning threshold

They are **not** your media. Your footage, references, and renders never enter this
repository.

---

## Sporsho Layer — Added

| Path | Contents |
|---|---|
| `SPORSHO/README.md` | Layer overview |
| `SPORSHO/BRAIN/` | Operating principles, routing, architecture |
| `SPORSHO/CLIENTS/` | Client profiles, editing rules, revision logs |
| `SPORSHO/REFERENCES/` | Reference analysis (markdown only) |
| `SPORSHO/EDITING-RULES/` | House style, cut rules, captions, audio, B-roll |
| `SPORSHO/PROMPTS/` | Prompt library |
| `SPORSHO/WORKFLOWS/` | Reusable production recipes |
| `SPORSHO/MEMORY/` | Learning loop |
| `SPORSHO/QC/` | Quality gates |
| `SPORSHO/INTEGRATIONS/` | Wiring documentation |
| `docs/sporsho/` | Integration, capability map, media, Arena, GitHub |

---

## Update Log

| Date | Action | Resulting commit |
|---|---|---|
| 2026-09-20 | Initial import of `08e2151` + Sporsho layer | _see `git log`_ |

Update this table after every `git merge upstream/main`, and refresh
`OPENMONTAGE_VERSION` above.
