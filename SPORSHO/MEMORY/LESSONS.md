# Lessons

What worked, what didn't. Newest first. Keep entries to the five-line contract in
[`README.md`](README.md).

Promote a lesson to a rule after it repeats three times, then mark it
`→ promoted to <file>`.

---

## Template

```markdown
### {{project-id}} — {{YYYY-MM-DD}}

**What we did:**   {{pipeline, register, client, duration}}
**What worked:**   {{specific and verifiable}}
**What didn't:**   {{specific and verifiable}}
**Surprise:**      {{something that behaved differently than documented}}
**Next time:**     {{one concrete, actionable change}}
```

---

## Entries

### radice-revision-top-tips — 2026-09-21

**What we did:**   Intake and source verification for a real client piece — 149.3 s, native
9:16 talking head, delivered as ten sequential chunks under a transfer size cap. All ten hashed
against recorded LFS OIDs, then rebuilt into one normalised master *before* any edit, then
measured for seam continuity, framing, and loudness.
**What worked:**   Refuse-to-proceed gates at every step (missing part, size mismatch, OID
mismatch, partial set) meant nothing downstream could quietly run on a bad source. Proving
"nothing missing or duplicated" by *pixel motion across each join vs motion either side of it*
(0.97–1.20× at all nine seams) instead of trusting that a clean decode implies a clean join.
Face-box geometry (forehead 23.5% from top, chin ≥644 px clear of the caption band) to decide
lower-third and punch-in limits with numbers rather than taste.
**What didn't:**   Three self-inflicted measurement failures, all of them mine, none of them the
media: (a) counting frames by grepping ffmpeg's stderr progress text returned `frame=0` for every
part; (b) the first master was built duration-driven (`fps` filter + concat demuxer) and silently
became 4483 frames, then 128 s of truncated audio; (c) a Laplacian-sharpness comparison across
1080p vs upscaled-720p crops reported the *softer* segment as sharper, because crop area and
gesture motion were not held constant.
**Surprise:**      `ffmpeg -f concat -c copy` of frame-exact chunks is not timestamp-safe. The
demuxer offsets each part by its *container* duration, which here overstated each part's frame
count by 0.4–22.7 ms; the join decoded without a single error while growing to **+0.2196 s of A/V
drift**, inventing two 66.7 ms "missing frame" gaps at two seams, and carrying 1080×1920 and
720×1280 in one MP4. That is how a correct edit ends up with narration and mouth movement
disagreeing more and more toward the end.
**Next time:**     For any split source, rebuild from **frame indices** (`setpts=N/(30*TB)` over
the whole concatenated stream, per-part PCM trimmed to `frames/fps`) as step one — never copy-join
then patch. Count frames with PyAV or `-count_frames`, never by parsing progress output. Run
`SPORSHO/QC/verify_master.py` and require PASS before the first cut, and again on the render.
Never quote a metric that hasn't been checked against a known-good file, and compare perceptual
metrics only at matched pixel scale.

*(First real-project entry. Newer entries go **above** this one.)*

---

## Seed Questions

When starting out, these are the questions worth answering most often. They target
the areas where OpenMontage gives you a default but your client may want something
different:

1. **Register accuracy** — Did the register you assumed match what the client wanted?
   If you had to ask, was the question clear?
2. **Hook performance** — Did the chosen opening line work, or did the client want
   a different one?
3. **B-roll relevance** — Did any insert illustrate a different sentence than the one
   under it? (`EDITING-RULES/BROLL-PACING.md` calls this the most common B-roll failure.)
4. **Jump-cut handling** — Did the chosen cover method (B-roll / punch-in / J-L cut)
   read as intentional or as a mistake?
5. **Caption readability** — Any complaints about size, contrast, or position?
6. **Audio balance** — Music too loud or too quiet on real playback devices?
7. **Tool surprises** — Did any tool behave differently than its skill file claims?
   (This is the highest-value category — see `FAULTS.md`.)
8. **Cost** — Did actual spend match the estimate? Where did it diverge?
