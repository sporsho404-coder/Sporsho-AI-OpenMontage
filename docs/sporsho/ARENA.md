# ARENA — How Arena Drives This System

How Arena connects to the repository and to `D:\SPORSHO AI`.

---

## The Model

```
YOU
 ↓  talk to
ARENA
 ↓  reads instructions from    ← the repo
SPORSHO/  +  OpenMontage core
 ↓  runs
TOOLS  (trim, compose, analyse, render)
 ↓  read/write
D:\SPORSHO AI   ← all heavy files
```

Arena is the orchestrator and agent runtime. It contributes **no** files to this
repository — it reads and executes.

---

## What Arena Must Read

### Every session

1. `AGENT_GUIDE.md` — upstream's mandatory contract. Upstream says to read it before
   responding to *any* message, and this repo preserves that instruction.
2. `SPORSHO/BRAIN/OPERATING-PRINCIPLES.md`
3. `SPORSHO/BRAIN/ROUTING.md`
4. `SPORSHO/MEMORY/INDEX.md` and `LESSONS.md`

### Per project

5. `SPORSHO/CLIENTS/<client>/PROFILE.md` and `EDITING-RULES.md`
6. The matching `SPORSHO/WORKFLOWS/*.md`
7. `SPORSHO/EDITING-RULES/` — all applicable files

### Before delivery

8. `SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`
9. `skills/meta/reviewer.md` — upstream's review protocol

---

## Configured Environment

For Arena or any agent runtime to use this repo, set:

```bash
export OPENMONTAGE_PROJECTS_DIR="/mnt/d/SPORSHO AI/projects"   # or Windows equivalent
export SPORSHO_ROOT="<path to this repo>"
export SPORSHO_MEDIA_ROOT="/mnt/d/SPORSHO AI"
```

Setting `SPORSHO_ROOT` and `SPORSHO_MEDIA_ROOT` is **Sporsho convention, not an
OpenMontage mechanism** — OpenMontage only knows `OPENMONTAGE_PROJECTS_DIR`. These
extra two are for your own scripts and prompts. Nothing upstream reads them.

---

## Prompt Contract

Every production turn should open with this routing block — this is OpenMontage's own
"Announce Before Execution" contract, with Sporsho context added:

```
Route:      reference | footage | generation | revision
Pipeline:   <real pipeline> (<stability>)
Client:     <client or HOUSE-STYLE>
Register:   urgent | steady | calm
Playbook:   <styles/*.yaml or styles/custom/*.yaml>
Rules:      <Sporsho rule files in play>
Tools:      <real tool names>
Media root: D:\SPORSHO AI\...
Est. cost:  <$ if paid providers involved>
```

Then execute. If any field is unknown, **ask before executing** — a wrong route costs
a render cycle.

---

## What Arena Must Not Do

1. **Write media into the repository.** Ever. See `LOCAL-MEDIA.md`.
2. **Edit upstream files to store Sporsho knowledge.** That breaks merges.
3. **Invent tool names.** Only names in `tools/` are real.
4. **Claim a capability without verifying it.** Check the registry first.
5. **Promise a provider without checking its key is configured.** The most common
   false promise in generated plans.
6. **Force-push, rewrite history, or change repo visibility** without explicit approval.
7. **Send client footage off the local machine** without explicit approval.
8. **Spend money** without confirming the budget.

---

## Session Opening Template

```markdown
## Context Loaded
- Route: {{...}}
- Client: {{...}}
- Memory read: {{N lessons relevant, summarised in one line each}}
- Media root: D:\SPORSHO AI (verified reachable: yes/no)

## Plan
{{what will happen, in the routing block format}}

## Approval Needed
{{anything requiring a gate per OPERATING-PRINCIPLES.md §9}}
```

---

## Session Closing Template

```markdown
## Delivered
- Project: {{id}}  →  {{path on D:\SPORSHO AI}}
- QC: pre-delivery ✅  short-form ✅ (if applicable)
- Reviewer protocol: ✅

## Memory Written
- `MEMORY/INDEX.md` — row added
- `MEMORY/LESSONS.md` — {{the one concrete lesson}}
- `CLIENT-TASTE.md` — {{updated / no change}}
- `FAULTS.md` — {{updated / no change}}

## Open Items
- {{anything unresolved}}
```

The closing block is not optional. It is what makes the next session smarter than
this one.
