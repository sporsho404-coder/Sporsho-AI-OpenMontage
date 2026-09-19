# Workflow: Talking-Head → Short-Form 9:16

- **Pipeline:** `talking-head` — **upstream stability: BETA** (rough edges expected)
- **For:** interview/talking-head clients needing vertical short-form
- **Typical:** 10–30 min source → 1–3 finished shorts of 30–60s
- **Cost drivers:** music generation, any image/video generation for B-roll, TTS if used

> **Beta warning:** upstream has not fully audited this pipeline. Mention it when
> routing here. Do not promise pristine behaviour.

---

## Inputs Required

- Source footage on `D:\SPORSHO AI\clients\<client>\footage\<project>\`
- `SPORSHO/CLIENTS/<client>/PROFILE.md` and `EDITING-RULES.md`
- Declared **register** (`urgent` / `steady` / `calm`) — ask if unclear
- Target count and target duration

## Steps

### 1. Intake & route
State the route block from `SPORSHO/BRAIN/ROUTING.md`. Confirm client, register, target.

### 2. Workspace init
Per OpenMontage's project-directory convention, initialise before any stage runs:

```bash
python -c "from lib.checkpoint import init_project; init_project('<project-id>', title='<Title>', pipeline_type='talking-head')"
```

`<project-id>` is kebab-case. With `OPENMONTAGE_PROJECTS_DIR` pointed at
`D:\SPORSHO AI\projects`, this lands in the right place (see `docs/sporsho/INTEGRATION.md`).

### 3. Transcribe
`transcriber` (whisper-based, offline by default) → word-level timestamps.
If `AZURE_SPEECH_KEY` is configured, `azure_stt` is preferred upstream.

**This artifact is the foundation of everything downstream.** Word timestamps are what
make word-boundary cutting possible. Do not proceed on a bad transcript.

### 4. Select the moment
Read the transcript for the strongest self-contained segment:

- Must stand alone without setup
- Must open on a strong line — see the Hook Rule in `EDITING-RULES/HOUSE-STYLE.md`
- Must land a payoff inside the target duration

Record why this segment was chosen. A selection without a reason cannot be reviewed.

### 5. Cut plan
Build the `edit_decisions` artifact per `skills/creative/video-editing.md`:

- `silence_cutter` first for dead air
- `video_trimmer` for filler words, false starts, duplicate takes
- Apply `EDITING-RULES/CUT-RULES.md` — never cut mid-word, preserve breath pauses
- Mark jump cuts and their planned covers

### 6. B-roll plan
Following `EDITING-RULES/BROLL-PACING.md`. Plan covers for jump cuts **now**, not later.

Source assets via `clip_search` / `direct_clip_search` / `pexels_video` / `pixabay_video`,
or generate with `image_gen` / `video_selector` if needed.

Record source + licence for every asset.

### 7. Music plan
**Mandatory step in OpenMontage** (`AGENT_GUIDE.md` → "Music Plan (Mandatory)").
Check which music tools are actually configured before promising one.

### 8. Captions
`subtitle_gen` → `remotion_caption_burn`, styled per
`EDITING-RULES/CAPTIONS-TYPOGRAPHY.md`. Validate contrast with
`lib/playbook_loader.validate_contrast()`.

### 9. Reframe to 9:16
`auto_reframe`. Do not centre-crop — it decapitates subjects. Verify subject framing
per `EDITING-RULES/HOUSE-STYLE.md`.

### 10. Compose
`video_compose` → `projects/<project-id>/renders/final.mp4`

### 11. Review
- OpenMontage's reviewer protocol: `skills/meta/reviewer.md` (CHAI rules — accurate,
  complete, constructive)
- Sporsho gate: `SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md`

### 12. Memory
Write to `SPORSHO/MEMORY/` — see that folder's README for the entry format.

---

## Rules In Play

- `SPORSHO/EDITING-RULES/HOUSE-STYLE.md` (register, hook rule, overlays)
- `SPORSHO/EDITING-RULES/CUT-RULES.md`
- `SPORSHO/EDITING-RULES/BROLL-PACING.md`
- `SPORSHO/EDITING-RULES/CAPTIONS-TYPOGRAPHY.md`
- `SPORSHO/EDITING-RULES/AUDIO-RULES.md`
- `SPORSHO/CLIENTS/<client>/EDITING-RULES.md` — **overrides all of the above**

## QC Gate

`SPORSHO/QC/PRE-DELIVERY-CHECKLIST.md` + `SPORSHO/QC/SHORT-FORM-QC.md`

## Memory Output

- Which segment was chosen and why
- Which cuts were made and the register used
- Any client rule that needed interpretation
- Any tool that behaved differently than its skill claimed

## Known Limitations

- `talking-head` is **beta** upstream
- Reference-based work is a *different* route — see `REFERENCE-TO-CONCEPT.md`
- This workflow does not do multi-speaker interview cutting; that needs a plan of its own
- Heavy generation costs money — budget must be confirmed before step 7
