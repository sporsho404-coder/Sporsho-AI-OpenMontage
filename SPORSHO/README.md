# SPORSHO — Customization Layer

> **This directory is yours. Everything outside it is upstream OpenMontage.**

This is the Sporsho AI customization layer. It sits *on top of* OpenMontage without
modifying it. The goal is simple and non-negotiable:

**OpenMontage must remain updatable. Your knowledge must remain permanent.**

---

## The Rule

```
SPORSHO/          ← you edit this freely. Never touched by upstream updates.
everything else/  ← upstream OpenMontage. Treat as read-only.
```

If you follow one rule, follow this one: **never edit OpenMontage core files to store
your own knowledge.** Put it in `SPORSHO/` and point OpenMontage at it using one of
the documented seams in [`../docs/sporsho/INTEGRATION.md`](../docs/sporsho/INTEGRATION.md).

---

## Folder Map

| Folder | What belongs here | Read by |
|---|---|---|
| `BRAIN/` | Master operating instructions. How Sporsho AI thinks, routes, and decides. | Arena / agent at session start |
| `CLIENTS/` | One folder per client: brand rules, tone, delivery specs, revision history. | Every project |
| `REFERENCES/` | Analysis of reference videos you admire. **Metadata only — no video files.** | Reference-driven work |
| `EDITING-RULES/` | Your house style: cut rules, pacing, J/L-cuts, captions, typography. | Edit stage |
| `PROMPTS/` | Your reusable prompt library, by category. | Generation stages |
| `WORKFLOWS/` | Repeatable end-to-end recipes tied to real OpenMontage pipelines. | Planning |
| `MEMORY/` | Lessons from shipped and failed edits. The learning loop. | Session start |
| `QC/` | Your quality gates and checklists, layers on top of OpenMontage's reviewer. | Pre-delivery |
| `INTEGRATIONS/` | How Arena, GitHub, and `D:\SPORSHO AI` plug together. | Setup / ops |

---

## Where Your Media Goes

**Never here.** GitHub holds intelligence, not footage.

| Asset | Lives on |
|---|---|
| Code, rules, prompts, workflows, metadata | This repo |
| Client footage, reference videos, renders, music, large assets | `D:\SPORSHO AI` |

See [`../docs/sporsho/LOCAL-MEDIA.md`](../docs/sporsho/LOCAL-MEDIA.md).

---

## Quick Start

1. Read [`BRAIN/OPERATING-PRINCIPLES.md`](BRAIN/OPERATING-PRINCIPLES.md) — the constitution.
2. Read [`../docs/sporsho/INTEGRATION.md`](../docs/sporsho/INTEGRATION.md) — the mechanical wiring.
3. Point OpenMontage's project root at your drive (one env var).
4. Add your first client under `CLIENTS/`.

---

## Honest Status

This layer defines **how** Sporsho works. Some of it wires into existing OpenMontage
seams today; some is a documented contract that requires a small amount of code before
it is machine-enforced.

Every file states which of the two it is. Nothing here claims a capability OpenMontage
does not have. See [`../docs/sporsho/CAPABILITY-MAP.md`](../docs/sporsho/CAPABILITY-MAP.md).
