# Workflow: Short-Form 9:16 (Vertical) Specifics

- **Applies to:** any vertical deliverable, regardless of pipeline
- **Tools:** `auto_reframe`, `remotion_caption_burn`, `video_compose`, `visual_qa`

This workflow is a **layer**, not a standalone route. Apply it on top of
`TALKING-HEAD-TO-SHORT.md` or `LONG-FORM-TO-CLIPS.md`.

---

## Vertical Is Not "Cropped Horizontal"

The single most common failure: centre-cropping a 16:9 frame to 9:16. It removes
the subject's head, hands, or the content they're demonstrating.

OpenMontage provides `tools/video/auto_reframe.py`. Use it. It exists precisely for this.

## Reframing Rules

| Source | Approach |
|---|---|
| Single speaker, centred | `auto_reframe` → verify head/hands in frame |
| Single speaker, off-centre | `auto_reframe` with subject tracking (`face_tracker` if needed) |
| Two speakers | Re-frame per speaker on their line, or split-frame |
| Screen demo / content | Do not crop — letterbox the content and put the speaker above or below |
| Wide shot with action | Track the action, not the people |

**Never** ship a vertical crop you have not visually verified. Check frames with
`frame_sampler` — the agent must actually look at them.

## Composition

- Subject in the **upper-middle** third
- **Lower third** reserved for captions
- Headroom: not so much that the subject is tiny, not so little that it's claustrophobic
- Keep the speaker's eyes on the upper third line

## Safe Zones

Keep text and key action clear of platform UI:

| Zone | Clear |
|---|---|
| Bottom ~15% | Progress bar, CTA, captions UI |
| Right edge ~12% | Like / comment / share stack |
| Top ~10% | Platform header / username |

`visual_qa` includes a caption occlusion check comparing brightness in the face zone
against the caption zone — run it.

## Duration Guidance

| Platform | Sweet spot | Hard ceiling |
|---|---|---|
| Shorts / Reels / TikTok | 20–45s | 60s for most content |
| Story formats | 15s or less | — |

Longer is not better. If a clip needs 90s to land, it probably needs a tighter edit,
not more runtime.

## Audio For Vertical

- Assume **phone speakers** unless told otherwise. Test the mix on a small speaker.
- Voice must be intelligible without headphones. Music bed lower than you'd use for TV.
- Captions are not optional — most vertical viewing is muted-at-start.

## QC Gate

`SPORSHO/QC/SHORT-FORM-QC.md`

## Known Limitations

- `auto_reframe` is automated; it can pick the wrong subject in busy frames — verify
- Split-screen layouts for multi-speaker need manual composition work
- Platform safe zones change without notice; treat the table above as a good default,
  not a permanent truth
