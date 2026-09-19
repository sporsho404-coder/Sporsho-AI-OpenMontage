# Sporsho AI — Architecture

How the layers relate, and — more importantly — **which files each layer owns.**

---

## Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ ARENA                                                       │
│ Conversation, orchestration, agent runtime.                 │
│ Owns: nothing in this repo.                                 │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ SPORSHO AI EDITING BRAIN            → SPORSHO/              │
│ Taste. Clients. House rules. Prompts. Memory. QC.           │
│ Owns: everything under SPORSHO/. Modifies nothing else.     │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ OPENMONTAGE PRODUCTION INTELLIGENCE → repo root (upstream)  │
│ AGENT_GUIDE.md · pipeline_defs/ · skills/ · .agents/skills/ │
│ styles/ · schemas/ · config.yaml                            │
│ Owns: production decisions. Updated by `git merge upstream`.│
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ EDITING / ANALYSIS / RENDERING TOOLS → tools/ · lib/        │
│ video_trimmer · video_compose · video_analyzer · audio_*    │
│ Owns: execution. Same every time. Never touched by Sporsho. │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ LOCAL FILES AND ASSETS              → D:\SPORSHO AI         │
│ Footage, references, renders, music, exports.               │
│ Owns: bytes. Never in git. Never uploaded.                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Ownership Matrix

| Concern | Owner | Lives in | Updatable by upstream? |
|---|---|---|---|
| Tool execution | OpenMontage | `tools/`, `lib/` | Yes |
| Pipeline definitions | OpenMontage | `pipeline_defs/` | Yes |
| Agent instructions | OpenMontage | `AGENT_GUIDE.md`, `AGENTS.md` | Yes |
| Vendor knowledge | OpenMontage | `.agents/skills/` | Yes |
| Look & feel presets | OpenMontage | `styles/*.yaml` | Yes |
| **Client identity** | **Sporsho** | `SPORSHO/CLIENTS/` | **No** |
| **House editorial rules** | **Sporsho** | `SPORSHO/EDITING-RULES/` | **No** |
| **Custom look playbooks** | **Sporsho** | `styles/custom/*.yaml` | **No** (separate dir) |
| **Prompt library** | **Sporsho** | `SPORSHO/PROMPTS/` | **No** |
| **Learning memory** | **Sporsho** | `SPORSHO/MEMORY/` | **No** |
| **Delivery QC gates** | **Sporsho** | `SPORSHO/QC/` | **No** |
| **Reference library** | **Sporsho** | `SPORSHO/REFERENCES/` | **No** |
| Media bytes | Local disk | `D:\SPORSHO AI` | No |

The whole design collapses to one sentence: **upstream owns machinery, Sporsho owns intent.**

---

## Why The Media Lives Outside Git

OpenMontage's own `.gitignore` already excludes `projects/`, `output/`, `pipeline/`,
`corpus/`, and `music_library/`. Upstream reached the same conclusion independently:
production assets are regenerable and must never be committed.

Sporsho extends that stance to client footage. A 60 GB client shoot in a git repo would
destroy the repo permanently — and git history cannot be shrunk without rewriting, which
would break every clone. This is not a style preference; it is a one-way door.

---

## The Upgrade Path

Because upstream history is preserved in this repository:

```bash
git fetch upstream
git merge upstream/main
```

The merge touches only upstream-owned paths. `SPORSHO/` is never in upstream's tree,
so it cannot conflict. This is the entire reason the layer exists as a separate top-level
directory rather than as edits scattered through the codebase.

If a merge ever *does* conflict inside `SPORSHO/`, that means someone edited upstream
files to store Sporsho knowledge — fix that immediately by moving the knowledge back
into `SPORSHO/`.
