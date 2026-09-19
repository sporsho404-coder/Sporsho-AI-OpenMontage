# Music Prompts

**Tools:** `music_gen`, `suno_music`, `fal_elevenlabs_music`, `google_music`,
`freesound_music`, `pixabay_music`, `music_library`, `comfyui_music`

**Skills:** `.agents/skills/music`, `skills/creative/sound-design.md`

---

## Music Planning Is Mandatory Upstream

`AGENT_GUIDE.md` contains a section titled **"Music Plan (Mandatory)"** under the
User-Facing Planning Protocol. Music is not an afterthought you add at the end — it is
planned before production.

Do not skip the music plan. OpenMontage will not let a production run quietly omit it,
and neither should you.

## Cheapest First

| Order | Option | Cost |
|---|---|---|
| 1 | `music_library` — your own tracks on `D:\SPORSHO AI\library\music\` | Free |
| 2 | `pixabay_music`, `freesound_music` | Free |
| 3 | `fal_elevenlabs_music`, `google_music` | Paid |
| 4 | `suno_music` | Paid |

**Your own library should be the first stop.** A curated library of 20 tracks you know
well beats generating a new one every time — faster, free, and consistent across a
client's videos.

Check which providers are configured before promising one. See
`SPORSHO/INTEGRATIONS/PROVIDERS.md`.

## Prompt Structure For Generation

```
[genre] + [mood] + [tempo in BPM] + [instrumentation] + [energy arc] +
[whether vocals] + [intended use]
```

Most music models handle genre and mood well, and **structure poorly.** If you need a
specific arc (build, drop, resolve) it is more reliable to generate a neutral bed and
shape it in the edit than to describe the arc and hope.

## Matching Music To Video

| Register | Tempo | Character |
|---|---|---|
| `urgent` | 120–140 BPM | Driving, percussive, minimal melodic distraction |
| `steady` | 95–115 BPM | Steady pulse, clean, supportive |
| `calm` | 60–90 BPM | Sparse, ambient, patient |

## Rules

1. **Plan before producing** — upstream's mandatory music plan.
2. **Check your library first.** Free and consistent.
3. **Confirm the provider is configured** before promising a track.
4. **No vocals under speech.** They compete for the same frequency band and destroy
   intelligibility. Instrumental only, unless voice is absent.
5. **One track per video.** Mixing beds mid-video reads as a mistake unless there's a
   deliberate act change.
6. **Fade at a musical boundary**, never mid-phrase (see `EDITING-RULES/AUDIO-RULES.md`).
7. **Duck, don't lower globally** — `audio_mixer` handles this.
8. **Record the track source and licence** in the project asset manifest.

## Library Curation

Track what you keep on `D:\SPORSHO AI\library\music\`:

```
library/music/
├── urgent/       ← 120-140 BPM, driving
├── steady/       ← 95-115 BPM, supportive
├── calm/         ← 60-90 BPM, ambient
└── LICENCES.md   ← source + licence per track (CRITICAL)
```

`LICENCES.md` matters more than the tracks. A track with no recorded licence is a
track you cannot safely ship to a client.

## Entries

_None yet._ Record generation prompts that produced keepers, and note which library
tracks work for which client.
