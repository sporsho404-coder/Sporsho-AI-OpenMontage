# WORKFLOWS — Reusable Production Recipes

Each workflow is an end-to-end recipe tied to a **real** OpenMontage pipeline.

---

## What A Workflow Is

A workflow is not a pipeline. OpenMontage owns pipelines
(`pipeline_defs/*.yaml` — stages, agents, checkpoints, budgets).

A workflow is the **Sporsho answer** to "we do this specific kind of job for this
specific kind of client, this way, every time, at this quality."

It glues together:

```
a real OpenMontage pipeline  +  a client profile  +  house rules  +  a QC gate
```

---

## Rules For Workflows

1. **Name a real pipeline.** If your workflow doesn't use one of the 13 existing
   pipelines, it is not a workflow — it is a feature request. Say so.
2. **Name real tools.** Tool names must exist in `tools/`. No invented names.
3. **State the stability.** `talking-head` and `clip-factory` are **beta** upstream.
   Say so in the workflow so nobody is surprised by rough edges.
4. **List the rules in play.** Which `EDITING-RULES/` files and which client rules apply.
5. **Define the QC gate.** Which `QC/` checklist closes it.
6. **Feed memory.** What gets written to `MEMORY/` when this workflow runs.

---

## Available Pipelines (reference table — do not invent others)

| Pipeline | Best for | Stability |
|---|---|---|
| `animated-explainer` | Topic → fully generated explainer | production |
| `talking-head` | Footage-led speaker videos | **beta** |
| `screen-demo` | Screen recordings, walkthroughs | production |
| `clip-factory` | Many clips from one long source | **beta** |
| `podcast-repurpose` | Podcast highlights, derivatives | **beta** |
| `cinematic` | Trailer, teaser, mood-led edit | production |
| `animation` | Motion-graphics / animation-first | production |
| `character-animation` | Rigged cartoon characters | beta |
| `hybrid` | Source footage + support visuals | production |
| `avatar-spokesperson` | Avatar / lip-sync presenter | production |
| `localization-dub` | Subtitle, dub, translate | beta |
| `documentary-montage` | Documentary-style montage | see manifest |
| `framework-smoke` | Minimal smoke test | test |

---

## Workflow Files

| File | Pipeline | Covers |
|---|---|---|
| [`TALKING-HEAD-TO-SHORT.md`](TALKING-HEAD-TO-SHORT.md) | `talking-head` | Raw interview → 9:16 short |
| [`REFERENCE-TO-CONCEPT.md`](REFERENCE-TO-CONCEPT.md) | varies | Reference video → your version |
| [`LONG-FORM-TO-CLIPS.md`](LONG-FORM-TO-CLIPS.md) | `clip-factory` | Long recording → clip set |
| [`SHORT-FORM-9x16.md`](SHORT-FORM-9x16.md) | `talking-head` / `clip-factory` | 9:16 specifics |
| [`REVISION-ROUND.md`](REVISION-ROUND.md) | any | Client feedback → re-delivery |

---

## Workflow File Template

```markdown
# Workflow: {{name}}

- **Pipeline:** {{real pipeline name}} ({{stability}})
- **For:** {{which clients / content type}}
- **Typical runtime:** {{source length → output length}}
- **Cost drivers:** {{which paid tools are involved}}

## Inputs Required
- {{footage path under D:\SPORSHO AI\...}}
- {{client profile}}
- {{anything that must be true before starting}}

## Steps
1. {{stage}} — agent/skill — tools — output artifact
2. ...

## Rules In Play
- SPORSHO/EDITING-RULES/{{file}}
- SPORSHO/CLIENTS/{{client}}/EDITING-RULES.md

## QC Gate
- SPORSHO/QC/{{checklist}}

## Memory Output
- {{what gets recorded after this run}}

## Known Limitations
- {{honest statement of what this workflow cannot do}}
```
