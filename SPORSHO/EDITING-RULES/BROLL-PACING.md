# B-roll & Pacing

**Tools:** `tools/video/clip_search.py`, `tools/video/direct_clip_search.py`,
`tools/video/pexels_video.py`, `tools/video/pixabay_video.py`, `tools/video/corpus_builder.py`,
`tools/video/clip_cache.py`, `tools/video/video_selector.py`, `tools/graphics/image_selector.py`
**Skills:** `skills/creative/broll-planning.md`, `skills/creative/long-form.md`,
`skills/creative/short-form.md`, `skills/creative/enhancement-strategy.md`

---

## Ownership

B-roll **planning method** is upstream — read `skills/creative/broll-planning.md`.
Sporsho owns the **selection taste** and the **pacing thresholds**.

---

## B-roll Selection Rules

### Relevance
- B-roll must illustrate the **specific** idea being spoken, not the general topic.
  For "we cut costs by 40%", show the *dashboard*, not a generic handshake.
- If the footage illustrates a different sentence than the one under it, it is wrong.

### Consistency
- Keep a consistent **look** within a video: same era, same saturation, same grain.
  `lib/variation_checker.py` catches drift; run it.
- Mixing stock with client footage: match grade with `color_grade`, do not leave a
  visibly different white balance between the two.
- Avoid obvious stock tropes. Specifically banned by house style:
  handshakes, high-fives, people pointing at whiteboards, typing with no screen visible,
  slow-motion laughing in an office.

### Legality
- Record the **licence and source** of every stock asset in the project's asset manifest
- Prefer licensed sources. Do not use footage whose provenance you cannot state.

---

## Pacing Rules

### Cover Frequency

| Register | B-roll coverage of runtime | Typical insert length |
|---|---|---|
| `urgent` | 20–35% | 0.8–1.5s |
| `steady` | 35–55% | 1.5–3.0s |
| `calm` | 40–70% | 3.0–6.0s |

Coverage above these ranges starts to feel like a slideshow with a voiceover.
`lib/slideshow_risk.py` flags exactly this — run it before delivery.

### Insert Placement
- Insert **after** the speaker establishes the idea, not before. The viewer needs the claim
  before the illustration.
- Return to the speaker within ~3s in `urgent` register. Long B-roll runs lose the face.
- Never insert B-roll over the hook line. Open on the speaker.

### Overlay vs B-roll
- Use **B-roll** when the idea is concrete and filmable
- Use **overlays/typography** when the idea is abstract, numeric, or a list
- Never both at once over the same sentence — competes for attention

---

## The Jump Cut ↔ B-roll Relationship

B-roll is Sporsho's **preferred** cover for a jump cut (see `CUT-RULES.md`).
This means the pacing plan and the cut plan must be built together — you cannot
plan B-roll after the cuts are locked without re-opening the cut list.

Order of operations:

```
transcript → cut decisions → identify jump cuts → plan B-roll covers → source assets → assemble
```

Not:

```
transcript → cut → assemble → "we should add some B-roll"
```

---

## Quality Gate Before Delivery

- [ ] Every B-roll insert illustrates the sentence it sits under
- [ ] Look/grade is consistent across all inserts
- [ ] Coverage within the register's range
- [ ] `lib/slideshow_risk.py` shows no slideshow risk
- [ ] `lib/variation_checker.py` shows no visual drift
- [ ] Every stock asset's source and licence recorded in the manifest
- [ ] No house-banned stock tropes
