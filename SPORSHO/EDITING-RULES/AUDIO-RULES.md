# Audio Rules

**Tools:** `tools/audio/audio_mixer.py`, `tools/audio/audio_enhance.py`,
`tools/analysis/audio_energy.py`, `tools/audio/music_gen.py`, `tools/audio/tts_selector.py`
**Skills:** `skills/creative/sound-design.md`, `.agents/skills/music`,
`.agents/skills/sound-effects`, `.agents/skills/elevenlabs`

---

## Target Levels

| Element | Target | Notes |
|---|---|---|
| Voice (integrated) | −16 LUFS | Platform standard for social |
| Music bed under voice | −18 to −22 LUFS | Relative to voice; voice always wins |
| Music only (no voice) | −14 LUFS | Can be louder when unopposed |
| True peak ceiling | −1.0 dBTP | Prevents codec clipping |
| Silence floor | below −60 dBFS | Digital silence, not near-silence |

`audio_enhance` handles loudness normalisation. Verify with `audio_probe` after mixing.

---

## Music

**Music selection is a mandatory planning step in OpenMontage** — see the
"Music Plan (Mandatory)" section of `AGENT_GUIDE.md`. Do not skip it, and do not
add music after the fact as an afterthought.

Choose by use of `tools/audio/music_gen.py` or the library tools
(`music_library`, `pixabay_music`, `freesound_music`, `google_music`,
`fal_elevenlabs_music`, `suno_music`) — check which are configured before promising one.

Sporsho rules:

- Music must **fade at a musical boundary**, never mid-phrase
- **Duck** under speech via `audio_mixer`; never lower the whole track globally to
  compensate — it makes music-absent sections hollow
- **One music bed per video** unless a deliberate act change
- Music ends 1–2s before the video's final frame, not cut off abruptly
- **Avoid** tracks with vocals under speech — they compete for the same frequency band
  and muddy intelligibility

## Sound Design

Use `skills/creative/sound-design.md` for technique. Sporsho additions:

- SFX supports the **cut**, not the content. A whoosh on every cut is noise.
- Use SFX at transitions that change time, place, or subject
- Keep SFX 6–10 dB below voice
- **Less is more.** Three well-placed SFX beat twenty scattered ones.

## Beat Sync

`tools/analysis/audio_energy.py` extracts energy/beat information. Use it to
align cuts to musical beats — but:

- **Only** in `urgent` register. Beat-locked cuts in `calm` register feel mechanical.
- Align **section changes** to beats, not every cut. Constant beat-locking is fatiguing.
- If the beat grid fights the speech rhythm, **speech wins.** Always.

---

## Voice

- TTS tool selection is a routing decision — use `tts_selector`, do not hardcode a provider
- Provider availability depends on configured API keys. **Check before promising.**
- Match TTS pacing to the declared register; a `calm` script read at `urgent` speed is a mismatch

## J-Cut / L-Cut Audio

The mechanic is upstream (`skills/creative/video-editing.md`). Sporsho operational notes:

- The 0.5s overlap is the default; extend to 0.7s for `calm` register
- Watch for phase issues if the same room tone appears on both sides of the overlap
- After any J/L-cut, **recheck caption sync** — timing shifts are a common defect
- `documentary-montage`'s compose-director documents L-cut ambient layering at 0.5–0.7
  volume under music; follow that pattern for ambience, not for dialogue
