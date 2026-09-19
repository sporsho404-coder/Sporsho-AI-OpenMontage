# Sporsho AI × OpenMontage

**The AI video-editing brain.** Private repository.

> **Why this file and not `README.md`?**
> `README.md` is upstream OpenMontage's README and is left byte-identical so that
> `git merge upstream/main` never conflicts. This file is the Sporsho entry point.
> Read this first; read `README.md` for OpenMontage itself.

---

## What This Repository Is

A **private** repository combining two things:

```
SPORSHO/            Your customization layer. Taste, clients, rules, memory, QC.
everything else/    OpenMontage — unmodified upstream core. The production engine.
```

The split exists so that **OpenMontage can be updated at any time without destroying
your custom knowledge.** See [`SPORSHO/INTEGRATIONS/UPSTREAM.md`](SPORSHO/INTEGRATIONS/UPSTREAM.md).

---

## The Architecture

```
┌───────────────────────────────────────────────────────────────┐
│ ARENA                                                         │
│ Conversation and orchestration.                               │
└────────────────────────────┬──────────────────────────────────┘
                             ↓
┌───────────────────────────────────────────────────────────────┐
│ SPORSHO AI EDITING BRAIN                    → SPORSHO/        │
│ Taste · clients · house rules · prompts · memory · QC         │
└────────────────────────────┬──────────────────────────────────┘
                             ↓
┌───────────────────────────────────────────────────────────────┐
│ OPENMONTAGE PRODUCTION INTELLIGENCE      → repo root upstream │
│ AGENT_GUIDE.md · pipeline_defs/ · skills/ · .agents/skills/   │
│ styles/ · schemas/ · config.yaml                              │
└────────────────────────────┬──────────────────────────────────┘
                             ↓
┌───────────────────────────────────────────────────────────────┐
│ EDITING / ANALYSIS / RENDERING TOOLS        → tools/ · lib/   │
│ video_trimmer · video_compose · video_analyzer · audio_*      │
└────────────────────────────┬──────────────────────────────────┘
                             ↓
┌───────────────────────────────────────────────────────────────┐
│ LOCAL FILES AND ASSETS                  → D:\SPORSHO AI       │
│ Footage · references · renders · music · exports              │
│ Never in git. Never uploaded.                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Start Here

| I want to… | Read |
|---|---|
| Understand how Sporsho thinks | [`SPORSHO/BRAIN/OPERATING-PRINCIPLES.md`](SPORSHO/BRAIN/OPERATING-PRINCIPLES.md) |
| Route a job correctly | [`SPORSHO/BRAIN/ROUTING.md`](SPORSHO/BRAIN/ROUTING.md) |
| See the layer/files map | [`SPORSHO/BRAIN/ARCHITECTURE.md`](SPORSHO/BRAIN/ARCHITECTURE.md) |
| Wire the system up | [`docs/sporsho/INTEGRATION.md`](docs/sporsho/INTEGRATION.md) |
| Know what actually exists | [`docs/sporsho/CAPABILITY-MAP.md`](docs/sporsho/CAPABILITY-MAP.md) |
| Set up the drive | [`docs/sporsho/LOCAL-MEDIA.md`](docs/sporsho/LOCAL-MEDIA.md) |
| Run a job end-to-end | [`SPORSHO/WORKFLOWS/`](SPORSHO/WORKFLOWS/) |
| Add a client | [`SPORSHO/CLIENTS/`](SPORSHO/CLIENTS/) |
| Ship something | [`SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`](SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md) |

---

## Capability Reality Check

Checked against the source at commit `08e2151` — **not assumed.**

**Already in OpenMontage** (use it, don't rebuild it):

✅ Reference-video analysis · ✅ reference-based editing decisions · ✅ talking-head
editing · ✅ 9:16 short-form · ✅ B-roll selection · ✅ pacing · ✅ cuts · ✅ J-cuts /
L-cuts · ✅ captions · ✅ typography · ✅ motion graphics · ✅ music · ✅ sound design ·
✅ visual consistency · ✅ quality control

**Genuine gaps the Sporsho layer fills:**

❌ Client-specific editing rules → [`SPORSHO/CLIENTS/`](SPORSHO/CLIENTS/)
❌ Revision handling → [`SPORSHO/WORKFLOWS/REVISION-ROUND.md`](SPORSHO/WORKFLOWS/REVISION-ROUND.md)
❌ Learning from successful/failed edits → [`SPORSHO/MEMORY/`](SPORSHO/MEMORY/)
❌ Multiple client profiles / project-specific instructions → [`SPORSHO/CLIENTS/`](SPORSHO/CLIENTS/)

**15 of 21 requirements already exist upstream. 2 are partial. 4 are missing.**
Full breakdown with evidence: [`docs/sporsho/CAPABILITY-MAP.md`](docs/sporsho/CAPABILITY-MAP.md).

---

## The One Rule

**Never edit OpenMontage core files to store Sporsho knowledge.**

Put it in `SPORSHO/`. If a merge ever conflicts inside `SPORSHO/`, something has gone
wrong. This rule is the entire reason the upgrade path works.

---

## Licence & Attribution ⚠️

**OpenMontage is licensed AGPL-3.0** — not MIT, not Apache.

- ✅ Private use is fine. No obligations triggered.
- ✅ Videos you produce are yours. AGPL covers software, not output.
- ⚠️ **Making this repository public** triggers distribution obligations.
- ⚠️ **AGPL §13:** hosting a modified OpenMontage over a network requires offering
  your modifications' source to users.

`LICENSE` is preserved **unmodified** (661 lines). The full 449-commit upstream
history is preserved, retaining every contributor's authorship. `upstream` remote
points at `calesthio/OpenMontage`.

**This repository is a derivative work. OpenMontage is the work of calesthio and its
contributors. Sporsho AI is the layer on top.**

Full analysis: [`docs/sporsho/INTEGRATION.md`](docs/sporsho/INTEGRATION.md) § The AGPL-3.0 Question.
Provenance record: [`PROVENANCE.md`](PROVENANCE.md).

---

## Keeping Current

```bash
git fetch upstream
git merge upstream/main
```

`SPORSHO/` cannot conflict — upstream's tree has no such directory. See
[`SPORSHO/INTEGRATIONS/UPSTREAM.md`](SPORSHO/INTEGRATIONS/UPSTREAM.md).

---

## Media Policy

| On GitHub | On `D:\SPORSHO AI` |
|---|---|
| Code, rules, prompts, workflows | Client footage |
| Client profiles, analysis notes | Reference videos |
| Memory, lessons, metadata | Renders, exports, music, assets |

Wire it with one variable, verified in `lib/paths.py`:

```bash
export OPENMONTAGE_PROJECTS_DIR="D:\SPORSHO AI\projects"
```

`D:\SPORSHO AI` never enters git. Git history cannot be shrunk — a 40 GB commit stays
forever. That door only opens once.
