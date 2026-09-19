# Integration — PROVIDERS

API keys, availability, and the most common planning mistake.

---

## The Rule That Prevents Most Failures

**A tool existing in the registry does not mean it is callable.**

OpenMontage registers ~100 tools. Many require API keys. A tool whose key is not
configured appears available but fails at call time.

**Always verify configuration before promising a provider.**

This is the single most common false promise in generated production plans:
the plan names Kling or Suno or HeyGen, and the run dies because no key exists.

---

## Key Locations

| What | Where |
|---|---|
| Supported keys (full list) | `.env.example` (upstream, committed) |
| Your actual keys | `.env` (**never committed**) |
| Credential loader | `lib/env_loader.py` |
| Google/Vertex service accounts | `GOOGLE_APPLICATION_CREDENTIALS` → a JSON path, **never committed** |

Upstream's `.gitignore` blocks `.env`, `.env.local`, `*.env`, `gcp-*.json`,
`*-service-account.json`, `service_account*.json`. Good — but **verify** before pushing.

---

## Providers By Category

Read `.env.example` for the authoritative, current list. Categories:

| Category | Providers (env key) |
|---|---|
| **Video generation** | FAL (`FAL_KEY`), Replicate (`REPLICATE_API_TOKEN`), Kling (`KLING_API_KEY`), MiniMax (`MINIMAX_API_KEY`), Runway (`RUNWAY_API_KEY`), Google/Veo (`GOOGLE_API_KEY`), Higgsfield (`HIGGSFIELD_API_KEY`) |
| **Image generation** | FAL, OpenAI (`OPENAI_API_KEY`), BFL/Flux, Recraft, Google Imagen |
| **TTS / voice** | ElevenLabs (`ELEVENLABS_API_KEY`), Azure (`AZURE_SPEECH_KEY`), OpenAI, Google, Fish Audio (`FISH_AUDIO_API_KEY`), Doubao (`DOUBAO_SPEECH_API_KEY`), DashScope |
| **Music** | Suno (`SUNO_API_KEY`), ElevenLabs via FAL, Pixabay, Freesound, Google |
| **Speech-to-text** | Local Whisper (**no key needed** — default), Azure (`AZURE_SPEECH_KEY`) |
| **Avatar / lip-sync** | HeyGen (`HEYGEN_API_KEY`), Kling |
| **Stock media** | Pexels (`PEXELS_API_KEY`), Pixabay (`PIXABAY_API_KEY`), Unsplash (`UNSPLASH_ACCESS_KEY`) |
| **Local GPU** | ComfyUI (`COMFYUI_SERVER_URL`), Modal (`MODAL_LTX2_ENDPOINT_URL`) |

---

## Free-First Strategy

Start with zero cost:

| Need | Free / local option |
|---|---|
| Transcription | `transcriber` (local Whisper) — **no key needed** |
| TTS | `piper_tts` (local) |
| Cutting, composing | ffmpeg-based tools — no API cost |
| Captions | `subtitle_gen` + `remotion_caption_burn` |
| Analysis | `video_analyzer`, `scene_detect`, `frame_sampler` |
| Local video gen | ComfyUI if you have a GPU |
| Music | `pixabay_music`, `freesound_music` (free tiers) |
| Stock | Pexels / Pixabay (free tiers) |

Add paid providers only where they change the outcome. Reference-video analysis,
cutting, captions, and QC cost nothing — which means your editorial brain can be
fully exercised before any spend.

---

## Cheap-First Rules

1. **Analyse and plan on free tools.** Never spend to discover what the edit should be.
2. **Confirm the plan with the user before paid generation.**
   That is the moment you know a render won't be wasted.
3. **Check `config.yaml` budget gates** — `budget.mode` is `observe` / `warn` / `cap`.
   `single_action_approval_usd` triggers approval on expensive calls.
4. **Cache aggressively.** `tools/video/clip_cache.py` and `tools/video/clip_embedder.py`
   exist for this. Re-generating an asset you already made is pure waste.
5. **Log actual vs estimated cost** to `SPORSHO/MEMORY/LESSONS.md` when they diverge.

---

## Availability Check

Before naming a provider in a plan:

```bash
# Which keys are actually set?
grep -oE '^[A-Z_]+' .env.example | while read -r k; do
  [ -n "${!k}" ] && echo "SET     $k" || echo "missing $k"
done
```

Or check `lib/env_loader.py` for the loader's own resolution logic.

---

## Secrets Hygiene

- `.env` on `D:\SPORSHO AI\.env` — **not** in the repo
- **Never** paste a key into a chat, a commit, or a memory entry
- **Never** commit a service-account JSON
- **If a key is ever committed:** rotate it immediately. Deleting the commit is not
  enough — it remains in history and in every clone.
- Use the pre-push hook in `docs/sporsho/GITHUB.md`; it scans for token patterns

## Rotation Log

Track rotations in `D:\SPORSHO AI\.env.rotations` (local, never committed):

```
2026-09-20  FAL_KEY           rotated — suspected exposure
2026-09-20  ELEVENLABS_API_KEY rotated — scheduled quarterly
```
