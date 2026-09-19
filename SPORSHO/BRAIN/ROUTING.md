# Sporsho AI — Routing

Decide the correct path **before** touching any tool. Misrouting is the most expensive
mistake in this system: it wastes money, renders, and client trust.

---

## The First Decision: What Did The User Actually Give You?

OpenMontage's own `AGENT_GUIDE.md` draws this line explicitly, and so do we.

```
Did they give a video as INSPIRATION ("make me something like this")?
   → REFERENCE-DRIVEN. Read skills/meta/video-reference-analyst.md
   → Sporsho context: SPORSHO/REFERENCES/

Did they give a video as MATERIAL ("edit this", "cut this up")?
   → FOOTAGE-DRIVEN. Use source_media_review + a footage-led pipeline.
   → Sporsho context: SPORSHO/CLIENTS/<client>/

Did they give neither ("make me a video about X")?
   → GENERATION-DRIVEN. Standard pipeline selection.
   → Sporsho context: SPORSHO/PROMPTS/ + HOUSE-STYLE.md

Are they asking about an existing edit ("here are my revision notes")?
   → REVISION. SPORSHO/CLIENTS/<client>/REVISION-LOG.md
```

Getting this wrong is the failure OpenMontage warns about by name: falling back to
"search the web and guess" when the user meant a reference workflow.

---

## Pipeline Routing Table

Only these pipelines exist. Do not reference others.

| Trigger | Pipeline | Upstream stability |
|---|---|---|
| Raw talking-head footage to edit | `talking-head` | **beta** |
| Long source → many short clips | `clip-factory` | **beta** |
| Podcast → highlights/derivatives | `podcast-repurpose` | **beta** |
| Footage + support visuals | `hybrid` | production |
| Trailer / teaser / mood-led | `cinematic` | production |
| Topic → fully generated explainer | `animated-explainer` | production |
| Motion-graphics / animation-first | `animation` | production |
| Screen recording / walkthrough | `screen-demo` | production |
| Documentary-style montage | `documentary-montage` | see manifest |
| Avatar / lip-sync presenter | `avatar-spokesperson` | production |
| Rigged cartoon characters | `character-animation` | beta |
| Subtitle / dub / translate | `localization-dub` | beta |
| Smoke test only | `framework-smoke` | test |

**Beta means beta.** Tell the user when you route into one. Upstream does not fully
audit them, and you should not imply otherwise.

---

## Capability → Real Tool Map

Downstream stages must use the actual tool names. These exist in `tools/`.

### Analysis
| Need | Tool |
|---|---|
| Reference/source deep analysis | `video_analyzer` |
| Transcript + word timestamps | `transcriber` (`whisperx` skill) |
| Subtitle fetching | `transcript_fetcher` |
| Scene boundaries | `scene_detect` |
| Frame extraction for review | `frame_sampler` |
| Audio energy / beat positions | `audio_energy` |
| Face tracking | `face_tracker` |
| Model-based understanding | `video_understand` |
| Automated visual QC | `visual_qa` |
| Composition validation | `composition_validator` |

### Cutting & Assembly
| Need | Tool |
|---|---|
| Execute cuts, trim, speed | `video_trimmer` |
| Remove dead air | `silence_cutter` |
| Final assembly | `video_compose` |
| Join segments | `video_stitch` |
| Reframe to 9:16 | `auto_reframe` |
| Caption burn-in | `remotion_caption_burn` |
| Subtitle file generation | `subtitle_gen` |

### Audio
| Need | Tool |
|---|---|
| Mix, ducking, fades, L-cut audio | `audio_mixer` |
| Loudness / cleanup | `audio_enhance` |
| Music generation | `music_gen`, `suno_music`, `fal_elevenlabs_music`, `freesound_music`, `pixabay_music`, `google_music` |
| TTS | `tts_selector` → `elevenlabs_tts`, `openai_tts`, `azure_tts`, `doubao_tts`, `fish_audio_tts`, `google_tts`, `kling_tts`, `piper_tts`, `dashscope_tts` |

### Visuals
| Need | Tool |
|---|---|
| Image generation | `image_gen` / `image_selector` |
| Stock imagery | `pexels_image`, `pixabay_image`, `unsplash` |
| Color grading | `color_grade` |
| Upscale | `upscale` |
| Face restore / enhance | `face_restore`, `face_enhance`, `eye_enhance` |
| Background removal | `bg_remove` |
| Captions / typography / motion graphics | Remotion via `video_compose`, plus `.agents/skills/` (GSAP, framer-motion, Remotion) |

### Validation Helpers
`lib/verify_scene_pacing.py`, `lib/variation_checker.py`, `lib/delivery_promise.py`,
`lib/slideshow_risk.py`, `lib/scoring.py`

---

## The Routing Answer Format

Always state, before executing:

```
Route:      [reference | footage | generation | revision]
Pipeline:   [name] ([stability])
Client:     [client or HOUSE-STYLE]
Playbook:   [styles/*.yaml or styles/custom/*.yaml]
Rules:      [Sporsho rule files in play]
Tools:      [the real tool names above]
Media root: D:\SPORSHO AI\...
Est. cost:  [$ if any paid provider is used]
```

This is OpenMontage's own "Announce Before Execution" contract from `AGENT_GUIDE.md`,
with the Sporsho layers added. Both contracts apply.
