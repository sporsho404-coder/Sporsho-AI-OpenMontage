# Workflow: Long-Form → Clip Set

- **Pipeline:** `clip-factory` (many clips from one long source) — **BETA upstream**
- **Also relevant:** `podcast-repurpose` (**beta**) for podcast inputs
- **For:** webinars, podcasts, long interviews, livestream VODs
- **Typical:** 45–120 min source → 5–15 clips

---

## Inputs Required

- Long source on `D:\SPORSHO AI\clients\<client>\footage\<project>\`
- Target clip count and per-clip duration band
- Platform per clip (may differ across clips — a source can yield both 16:9 and 9:16)
- Client profile + register

## Steps

### 1. Transcribe once, everything downstream
`transcriber` → word-level timestamps. For long sources this is the expensive step
in wall-clock time. Do it once and cache it.

### 2. Segment the source
Break into topically coherent units. For each candidate, record:
- Topic in one sentence
- Self-contained? (understandable without the preceding 5 minutes)
- Has a hook line? Where?
- Has a payoff? Where?

### 3. Score candidates
Rank by: hook strength, self-containment, payoff strength, relevance to the client's
audience. Drop anything that needs context to make sense — those clips always
underperform.

Present the ranked shortlist to the user **before** cutting. Cutting 15 clips that
get rejected is a waste of a render cycle.

### 4. Per-clip production
Each selected clip runs the `TALKING-HEAD-TO-SHORT.md` sequence from step 4 onward:
moment selection → cut plan → B-roll → captions → reframe → compose.

### 5. Batch QC
QC every clip against `SPORSHO/QC/SHORT-FORM-QC.md`, plus:
- Consistency across the set (same grade, same caption style, same music family)
- No two clips make the same point
- No clip repeats another's hook

## Rules In Play

- `SPORSHO/EDITING-RULES/` — all files
- Client rules override

## QC Gate

`SPORSHO/QC/SHORT-FORM-QC.md` applied per clip + set-level consistency review.

## Memory Output

- Which topics the client approved vs rejected, with reasons
- Which duration band performed best (once you have platform data)
- Hook patterns that survived the client's judgement

## Known Limitations

- `clip-factory` and `podcast-repurpose` are both **beta** upstream
- Automatic segmentation still needs human judgment on what is *interesting* —
  the tools find *candidate* moments, not *good* ones
- Set-level consistency is not automatically enforced; you must check it
- Cost scales linearly with clip count once generation is involved
