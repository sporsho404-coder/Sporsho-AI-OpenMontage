# Sporsho AI — Operating Principles

**Layer:** Sporsho AI Editing Brain (above OpenMontage Production Intelligence)
**Status:** Authoritative for all Sporsho work.

---

## 1. What Sporsho Is

Sporsho AI is the **editorial brain**. OpenMontage is the **production engine**.

Sporsho decides *what the video should be* — the taste, the client fit, the pacing,
the rules and the memory of what worked. OpenMontage decides *how to actually build it* —
which tools, which providers, which pipeline, which render runtime.

Sporsho does not reimplement OpenMontage. That is the single biggest failure mode to avoid.

---

## 2. The Stack

```
Arena                          ← you talk to this. Orchestration + agent runtime.
   ↓
Sporsho AI Editing Brain       ← SPORSHO/ — taste, clients, rules, memory, QC.
   ↓
OpenMontage Production Intel.  ← upstream — pipelines, skills, providers, agents.
   ↓
Editing / Analysis / Rendering ← tools/ — trim, compose, analyze, generate, render.
   ↓
D:\SPORSHO AI                  ← footage, references, renders, music. Never in git.
```

Each layer owns exactly one concern. Do not let a lower layer hold state that
belongs to a higher one, and do not let a higher layer duplicate a lower one's job.

---

## 3. Rule Zero — Inherited From OpenMontage

OpenMontage's own `AGENT_GUIDE.md` states: **all production goes through a pipeline.**
Sporsho inherits this without exception.

Never hand-build a video file-by-file when a pipeline exists. If no pipeline fits,
say so and propose a new pipeline manifest rather than improvising a one-off.

---

## 4. Read Order At Session Start

Before responding to any Sporsho production request, load in this order:

1. `SPORSHO/BRAIN/OPERATING-PRINCIPLES.md` — this file
2. `SPORSHO/BRAIN/ROUTING.md` — decide reference-work vs footage-work vs generation
3. `SPORSHO/MEMORY/INDEX.md` — what we learned last time
4. `SPORSHO/CLIENTS/<client>/PROFILE.md` — if a client is named
5. `AGENT_GUIDE.md` (upstream) — the authoritative OpenMontage contract

OpenMontage's `AGENTS.md` says to read `AGENT_GUIDE.md` before responding to *any*
user message. That instruction is upstream's and remains in force. Sporsho adds
context on top; it never replaces it.

---

## 5. Never Duplicate OpenMontage

Before adding anything to `SPORSHO/`, ask: **does OpenMontage already do this?**

| If OpenMontage already has… | Then Sporsho does NOT… |
|---|---|
| `tools/video/video_trimmer.py` | write its own cutting code |
| `skills/creative/video-editing.md` (J-cut/L-cut/pacing) | restate general editing theory |
| `skills/meta/video-reference-analyst.md` | build a second reference analyzer |
| `skills/meta/reviewer.md` + `tools/analysis/visual_qa.py` | build a parallel QC system |
| 13 pipeline manifests | invent a competing orchestration layer |
| `styles/*.yaml` playbooks | hardcode look-and-feel in prose |

Sporsho **configures** and **constrains** those. It does not fork them.

---

## 6. Where Sporsho Genuinely Adds Value

These are real gaps in OpenMontage as inspected at commit `08e2151`. Verified by
searching the source — not assumed.

| Gap | Status upstream | Sporsho supplies |
|---|---|---|
| Client profiles / per-client rules | **Does not exist** (0 references in source) | `SPORSHO/CLIENTS/` |
| Client revision rounds | **Does not exist** (upstream `max_revisions_per_stage` is *stage send-backs*, not client feedback) | `CLIENTS/*/REVISION-LOG.md` |
| Learning from past edits | **Does not exist** (no retrospective artifact) | `SPORSHO/MEMORY/` |
| House editorial style as enforced rules | Partially — playbooks cover look, not cut behaviour | `SPORSHO/EDITING-RULES/` |
| Reusable prompt library | `PROMPT_GALLERY.md` exists upstream (generic) | `SPORSHO/PROMPTS/` (yours) |
| Project-specific instructions | Project dirs are gitignored & regenerable | `SPORSHO/WORKFLOWS/` + client profiles |

Everything else — analysis, cutting, captions, audio, rendering, QC mechanics —
**OpenMontage already does it. Wire into it.**

---

## 7. Client Work Is Never Generic

If a client is named, their `PROFILE.md` and `EDITING-RULES` override Sporsho defaults.
If a client rule conflicts with an OpenMontage default, the client rule wins for that
client's work — but log the conflict in the client folder so it stays visible.

If no client is named, use `SPORSHO/EDITING-RULES/HOUSE-STYLE.md`.

---

## 8. Confidence And Honesty

- Never claim OpenMontage can do something you have not verified in its source.
- Never invent a tool name. Tool names come from `tools/` and the registry.
- When a capability is missing, say **"this needs to be built"** and say where it belongs.
- Partial capabilities are stated as partial. `talking-head` and `clip-factory` are
  marked **beta** upstream — say so when recommending them.

---

## 9. Approval Gates

Stop and ask before:

- Deleting or restructuring anything outside `SPORSHO/`
- Force-pushing, rewriting history, or changing repository visibility
- Making the repository public (see the licence warning in `docs/sporsho/INTEGRATION.md`)
- Sending client footage anywhere off the local machine
- Spending money through a paid provider tool
- Committing anything over ~10 MB, or any credential

---

## 10. The Definition Of Done

A Sporsho edit is done when **all four** are true:

1. It satisfies the client profile and their editing rules.
2. It passes `SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`.
3. It passed OpenMontage's own reviewer protocol (`skills/meta/reviewer.md`).
4. What was learned got written to `SPORSHO/MEMORY/`.

Point 4 is what makes this a brain instead of a tool. Do not skip it.
