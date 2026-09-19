# Editing Rules — House Style

**Applies to:** all Sporsho work unless a client profile overrides it.
**Layer:** Sporsho. Client rules win on conflict.

OpenMontage already documents general editing craft in `skills/creative/video-editing.md`
(filler words, false starts, J-cut, L-cut, pacing by duration) and
`skills/creative/video-stitching.md`. **Those rules are inherited, not repeated here.**

This file records only what Sporsho decides *differently or additionally*.

---

## Inherited From OpenMontage (do not restate, do not override lightly)

- Cut filler words, false starts, dead air >1.5s, tangents, duplicate takes
- Keep breath pauses (0.3–0.8s) and emphasis pauses
- J-cut: next segment's audio starts ~0.5s before the visual cut
- L-cut: current segment's audio continues ~0.5s past the visual cut
- Hard cut at major topic changes
- Cut at word boundaries, never mid-word
- Pacing by duration: short-form aggressive, medium balanced, long-form breathing room

Source of truth: `skills/creative/video-editing.md`. Read it; do not copy it.

---

## Sporsho Additions

### House Defaults

| Parameter | House value | Rationale |
|---|---|---|
| Min shot hold | 0.8s | Below this reads as a glitch, not a cut |
| Max shot hold (talking head) | 6.0s | Beyond this attention drops on 9:16 |
| Dead-air trim floor | 0.5s | Harder trim feels clipped |
| J/L-cut overlap | 0.5s (inherited) | Matches upstream default |
| Caption max words/card | 7 | Readable at 9:16 mobile size |
| Music bed under voice | −18 LUFS | Voice stays intelligible |
| Silence window before hook | 0.3s | Gives the first line room |

### Cut Register

Every project declares one register. It governs pacing decisions downstream.

| Register | Shot hold | Cut style | Use for |
|---|---|---|---|
| `urgent` | 0.8–2.0s | Hard cuts, jump cuts on emphasis | Hooks, shorts |
| `steady` | 1.5–4.0s | J/L-cuts, soft transitions | Corporate, explainer |
| `calm` | 3.0–8.0s | Long holds, few cuts, breathing room | Documentary, testimony |

If the client's tone is unclear, ask. Do not guess the register.

### The Hook Rule

The first 3 seconds decide the video. For any short-form deliverable:

- Open on the strongest line, not the introduction
- No logo intros, no title cards before the hook
- If the source's first line is weak, find the strongest line later in the
  transcript and open there — state that you did this

### Overlay Discipline

- Never cover the speaker's face or hands
- One idea per overlay; if an overlay needs two sentences, it is a scene, not an overlay
- Text must clear WCAG AA contrast — `lib/playbook_loader.py` provides
  `validate_contrast()` and `check_color_blind_safety()`; use them

### Audio

- Voice is always the anchor. Music never competes with it.
- Duck music under speech; OpenMontage's `audio_mixer` handles this
- No music that starts or ends mid-phrase — fade at a musical boundary

---

## Visual Consistency

OpenMontage provides enforcement, use it rather than hand-checking:

- `lib/variation_checker.py` — catches scenes that drift too far from each other
- `lib/slideshow_risk.py` — flags edits that read as a slideshow
- `lib/verify_scene_pacing.py` — checks pacing against declared rules
- `lib/delivery_promise.py` — checks the output matches what was promised

**Sporsho rule:** run these before delivery, not after a client notices.

---

## 9:16 Short-Form Specifics

- Reframe with `auto_reframe`. Do not crop centre-first — it cuts heads off.
- Subject should sit in the upper-middle third; leave the lower third for captions
- Safe zones for platform UI (captions, buttons) apply — keep text clear of the
  bottom ~15% and right edge
