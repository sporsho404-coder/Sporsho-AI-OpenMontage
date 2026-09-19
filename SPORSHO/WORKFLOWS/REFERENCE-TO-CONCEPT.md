# Workflow: Reference Video → Your Version

- **Pipeline:** determined after analysis (often `animated-explainer`, `cinematic`, or `hybrid`)
- **For:** "make me something like this" requests
- **Typical:** reference URL → 2–3 differentiated concepts → selected concept → production

---

## This Is A Distinct Route

OpenMontage's `AGENT_GUIDE.md` is explicit: reference-driven requests must **not** be
treated as generic web-search or prompt-writing requests. The failure mode named
upstream is exactly that — a model falls back to search-and-guess.

Trigger phrases: *"something like this"*, *"inspired by"*, *"I love this Reel"*,
*"in this style"*, *"similar to"*.

## Inputs Required

- Reference URL or local file
- Target platform / duration
- Client (if any)
- Whether originality matters (is this "inspired by" or "clone the format"?)

## Steps

### 1. Analyse via OpenMontage (do not build a second analyzer)

Read and follow `skills/meta/video-reference-analyst.md`. Run:

```python
video_analyzer.execute({
    "source": "<url or path>",
    "analysis_depth": "standard",
    "max_keyframes": 20
})
```

Supporting tools: `scene_detect`, `frame_sampler`, `transcriber`, `transcript_fetcher`.

### 2. Present the summary conversationally

**This is upstream's required behaviour, not optional.** Structure it by the 5 aspects
so downstream stages can lift fields directly:

- Content · Style · Structure · Motion
- 5-aspect breakdown: Subject · Subject Motion · Scene · Spatial Framing · Camera
- "What makes it work" — 2–3 specifics

Do not dump raw JSON.

### 3. Store the intelligence

Write to `SPORSHO/REFERENCES/<slug>/`:
- `ANALYSIS.md` — the structured brief
- `PATTERNS.md` — generalised, reusable techniques
- `source.md` — provenance
- Add a row to `SPORSHO/REFERENCES/INDEX.md`

**Never** store the video file in the repo. Bytes go to `D:\SPORSHO AI\references\`.

### 4. Capability audit

Before proposing concepts, verify the tools exist and are configured.

- Check the tool registry for what is actually available
- Check which providers have API keys configured
- **Do not propose concepts that require unconfigured providers**

### 5. Propose 2–3 differentiated concepts

Upstream requires **2–3**, and they must be **differentiated** — not the same idea
three ways, and **not a carbon copy** of the reference.

Each concept states:

```
Concept:    {{name}}
Angle:      {{how it differs from the reference and from the other concepts}}
Pipeline:   {{real pipeline + stability}}
Register:   {{urgent | steady | calm}}
Tools:      {{real tool names}}
Est. cost:  {{$}}
Risk:       {{what could go wrong}}
```

### 6. Produce

Follow the selected concept through the normal pipeline. Client rules and
`SPORSHO/EDITING-RULES/` apply from here on.

### 7. Memory

Record which concept the user chose **and which they rejected**. Rejection reasons are
the highest-value learning signal in this workflow — they reveal taste that isn't
written down anywhere yet. If a rejection reason recurs, promote it to a rule.

## Rules In Play

- `SPORSHO/EDITING-RULES/HOUSE-STYLE.md`
- `SPORSHO/REFERENCES/<slug>/PATTERNS.md` — extracted patterns feed the concepts
- Client rules if a client is named

## QC Gate

`SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`, plus a check that the output is
**inspired by**, not a **copy of**, the reference.

## Known Limitations

- Reference analysis quality depends on the source's audio/video quality
- Some reference videos use techniques with no equivalent tool here — say so honestly
  rather than proposing an imitation that will disappoint
- Copyright: emulating a *format* is normal; reproducing *content* is not. Flag it if
  the reference's value is the content rather than the technique.
