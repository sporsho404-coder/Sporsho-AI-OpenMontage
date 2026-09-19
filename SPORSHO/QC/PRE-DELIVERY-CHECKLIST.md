# Pre-Delivery Checklist

**Nothing ships without passing this.** Copy into the project and tick it, or work
through it and record the result.

---

## Layer 1 — OpenMontage's Own Review (do not skip)

- [ ] Reviewer protocol run per `skills/meta/reviewer.md`
- [ ] CHAI rules applied: **Accurate** (every finding cites a concrete artifact field),
      **Complete** (scanned for the rest of the same class), **Constructive**
      (every critical finding proposes a fix)
- [ ] Every artifact validated against `schemas/artifacts/*.schema.json`
- [ ] All checkpoints honoured per the pipeline's checkpoint policy
- [ ] Budget respected; no unapproved spend

Run these automated checks — they cover things humans miss:

- [ ] `lib/verify_scene_pacing.py` — pacing matches declared rules
- [ ] `lib/variation_checker.py` — no unintended visual drift
- [ ] `lib/slideshow_risk.py` — output doesn't read as a slideshow
- [ ] `lib/delivery_promise.py` — output matches what was actually promised

## Layer 2 — Technical (automated)

- [ ] `tools/analysis/visual_qa.py` run — frame checks, transition verification
- [ ] `visual_qa` caption occlusion check shows no face/caption overlap
- [ ] `tools/analysis/audio_probe.py` — loudness within target, no clipping
- [ ] Loudness: voice ≈ −16 LUFS, true peak ≤ −1.0 dBTP
- [ ] Resolution, codec, and frame rate match the client's spec exactly
- [ ] Duration within the agreed band
- [ ] File naming matches the client's convention
- [ ] Final render opens and plays end-to-end without corruption

## Layer 3 — Sporsho Editorial

### Cut
- [ ] No cut lands mid-word
- [ ] No unintended jump cut is visible
- [ ] Intended jump cuts are covered (B-roll / punch-in / J-L cut)
- [ ] Shot holds within the declared register's range
- [ ] Transitions match the register (no stray dissolves in `urgent`)

### Audio
- [ ] Voice intelligible on a **phone speaker**, not just headphones
- [ ] Music fades at a musical boundary
- [ ] No audible clicks or pops at cut points
- [ ] J/L-cut overlaps do not phase or double-room-tone
- [ ] Captions still in sync **after** any timing-shifting edit

### Captions & Type
- [ ] ≤ 7 words per card, ≤ 2 lines
- [ ] Contrast passes WCAG AA — verified with `lib.playbook_loader.validate_contrast()`,
      not by eye
- [ ] Colour-blind safety checked via `check_color_blind_safety()` if colour carries meaning
- [ ] Clear of platform UI safe zones
- [ ] No missing-glyph boxes (emoji, special characters)

### Visual
- [ ] 9:16 outputs submitted to `SPORSHO/QC/SHORT-FORM-QC.md`
- [ ] Grade consistent across all sources and inserts
- [ ] No overlay covers the speaker's face or hands
- [ ] Every B-roll insert illustrates the sentence it sits under

### Client
- [ ] Every rule in `CLIENTS/<client>/EDITING-RULES.md` applied
- [ ] Every stated non-negotiable respected
- [ ] No known client dislike present in the output
- [ ] Divergences from house style are logged in the client's `REVISION-LOG.md`

## Layer 4 — Delivery

- [ ] Deliverable in the format the client asked for, not the format we prefer
- [ ] All source/licence records complete for third-party assets
- [ ] Revision round count vs. contract checked (`CLIENTS/<client>/DELIVERY.md`)
- [ ] Client notified with a summary of what changed and why

## Layer 5 — Memory (this is the one people skip)

- [ ] Row added to `SPORSHO/MEMORY/INDEX.md`
- [ ] Entry added to `SPORSHO/MEMORY/LESSONS.md` with a concrete "Next time"
- [ ] `CLIENT-TASTE.md` updated if you learned something about them
- [ ] `FAULTS.md` updated if any tool surprised you
- [ ] Recurring lessons promoted to rules

**If Layer 5 is incomplete, the project is not finished.** Everything above makes one
good video. Layer 5 is what makes the next one better.
