# REFERENCES — Reference Video Intelligence

Analysis of videos worth learning from. **Metadata only. No video files. Ever.**

---

## OpenMontage Already Owns Reference Analysis

This is important: **do not build a second analyzer.**

OpenMontage treats reference-video work as a first-class workflow. It has:

- `AGENT_GUIDE.md` → "Reference Video Entry Point" — the mandatory behaviour
- `skills/meta/video-reference-analyst.md` — the full analysis protocol
- `tools/analysis/video_analyzer.py` — the engine
- `tools/analysis/scene_detect.py`, `frame_sampler.py`, `transcriber.py` — supporting tools

When the user says "make me something like this," the correct action is to **run
OpenMontage's reference workflow**, then store the resulting intelligence here.

**Sporsho's job is to remember the output, not to produce it.**

---

## What Goes Here

For each reference video, one markdown file:

```
REFERENCES/
├── README.md                     ← this file
├── INDEX.md                      ← all references, one line each
└── <slug>/
    ├── ANALYSIS.md               ← the OpenMontage VideoAnalysisBrief + your read
    ├── PATTERNS.md               ← what's reusable, generalised
    └── source.md                 ← URL, creator, date, why it's worth learning from
```

## What Must NOT Go Here

- ❌ `.mp4` / `.mov` files — these live on `D:\SPORSHO AI\references\`
- ❌ Downloaded stock clips
- ❌ Thumbnails and frames (unless tiny and genuinely load-bearing)
- ❌ Anything copyrighted that you would be redistributing by pushing to GitHub

`source.md` records the **URL**. The bytes stay local. This keeps the repository
light and keeps you out of copyright trouble.

---

## How To Capture A Reference

```
1. User provides a URL or local file.
2. Run OpenMontage's reference workflow (skills/meta/video-reference-analyst.md).
3. Present the summary conversationally to the user — this is upstream's
   required behaviour, not optional.
4. Save the structured output to REFERENCES/<slug>/ANALYSIS.md.
5. Extract the GENERALISABLE patterns to PATTERNS.md.
6. Record provenance in source.md.
7. Add one line to INDEX.md.
```

Step 5 is the Sporsho addition. A one-off analysis of one video is not knowledge.
A generalised pattern is.

---

## The ANALYSIS.md Shape

Use OpenMontage's own 5-aspect breakdown — it exists so downstream stages can lift
fields directly. Do not invent a different structure.

```markdown
# Reference: {{title}}

## Provenance
- URL: {{url}}
- Creator: {{name}}
- Length: {{mm:ss}}
- Why it matters: {{1 sentence}}

## Summary
**Content:**   {{2 sentences}}
**Style:**     {{1 sentence — pacing, treatment, energy}}
**Structure:** {{N scenes over Y seconds, pacing style}}
**Motion:**    {{N of M scenes motion clips / animated stills / static}}

## 5-Aspect Breakdown
- Subject:
- Subject Motion:
- Scene:            (overlays listed separately)
- Spatial Framing:
- Camera:

## What Makes It Work
1. {{specific technique}}
2. {{specific technique}}
3. {{specific technique}}

## Extracted Patterns
→ see PATTERNS.md

## Cost To Emulate
{{What would it cost in tools and time to produce something like this?}}
```

---

## PATTERNS.md — The Valuable Part

This is where a reference stops being a curiosity and becomes reusable intelligence.

```markdown
# Patterns From: {{title}}

## Pattern: {{name}}
- **What:** {{the technique in one sentence}}
- **When to use:** {{trigger condition}}
- **How to build:** {{real tool names from tools/}}
- **Register fit:** urgent | steady | calm
- **Risk:** {{what goes wrong when you get it wrong}}
```

Patterns get referenced by `SPORSHO/WORKFLOWS/` and by client rules. A pattern that
never gets referenced is dead weight — if a pattern is not used within a few projects,
consider deleting it.
