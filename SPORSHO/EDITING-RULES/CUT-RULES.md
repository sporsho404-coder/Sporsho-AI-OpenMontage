# Cut Rules

Sporsho-specific cut behaviour. General cut craft is upstream
(`skills/creative/video-editing.md`, `skills/creative/video-stitching.md`).

**Executed by:** `tools/video/video_trimmer.py`, `tools/video/silence_cutter.py`,
`tools/video/video_compose.py`, `tools/video/video_stitch.py`

---

## Which Tool Does What

| Job | Tool | Note |
|---|---|---|
| Execute keep-segments with in/out points | `video_trimmer` | Reads `edit_decisions.cuts` |
| Remove dead air at scale | `silence_cutter` | Use before manual trimming |
| Splice segments with transitions | `video_stitch` | Handles J/L-cut overlap |
| Assemble the final timeline | `video_compose` | Final step |

Order matters: `silence_cutter` → `video_trimmer` → `video_stitch` → `video_compose`.

---

## The Edit Decision Contract

`video_trimmer` consumes the `edit_decisions` artifact described in
`skills/creative/video-editing.md`:

- `cuts` — ordered keep segments (source, in/out, speed)
- `overlays` — timed overlay placements
- `subtitles` — caption configuration
- `music` — asset, volume, ducking, fades
- `transitions` — type and timing

**Write every cut with a reason.** A cut list without reasons cannot be reviewed,
cannot be learned from, and cannot be defended to a client.

```yaml
cuts:
  - source: take_03.mp4
    in: 12.40
    out: 18.92
    speed: 1.0
    reason: "Strongest delivery of the core claim; take_01 had a false start"
  - source: take_03.mp4
    in: 19.10
    out: 24.05
    speed: 1.0
    reason: "Payoff line, kept intact"
```

---

## Jump Cut Handling

Jump cuts are the defining problem of talking-head editing. Options, in order of preference:

1. **Hide under B-roll** — cover the cut with a relevant insert. Best result, costs an asset.
2. **Punch-in** — scale to 105–115% on the second segment. Cheap, standard, effective.
3. **J/L-cut through it** — let audio carry across the visual seam.
4. **Leave it** — acceptable in `urgent` register short-form; distracting in `calm`.

Never apply a transition effect (dissolve, wipe) to hide a jump cut in talking-head work.
It reads as amateur. This is a Sporsho house position.

---

## Trim Discipline

- **In-points:** start 1–2 frames *before* the word begins, not on it. Audible ease-in.
- **Out-points:** end 1–2 frames *after* the word ends. Cutting flush sounds clipped.
- **Never** cut inside a word, ever — use word timestamps from `transcriber`.
- **Preserve** breath pauses 0.3–0.8s (upstream rule).
- **Preserve** deliberate emphasis pauses even above 1.5s if they serve the delivery.

## Speed Changes

- 1.0–1.08× — imperceptible, use freely to recover timing
- Above 1.10× — audible pitch/rhythm shift, only when the client accepts it
- Below 1.0× — almost never; only for deliberate dramatic slow-down of B-roll

## Transitions

| Register | Default transition |
|---|---|
| `urgent` | Hard cut |
| `steady` | Hard cut, J/L-cut for dialogue |
| `calm` | Hard cut, occasional 6–10 frame dissolve |

Dissolves over 12 frames read as "corporate video from 2009." Keep them short or absent.
