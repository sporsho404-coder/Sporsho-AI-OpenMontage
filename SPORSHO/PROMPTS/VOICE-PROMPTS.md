# Voice Prompts

**Tools:** `tts_selector` → `elevenlabs_tts`, `openai_tts`, `azure_tts`, `google_tts`,
`doubao_tts`, `fish_audio_tts`, `kling_tts`, `piper_tts`, `dashscope_tts`, `fal_elevenlabs_tts`

**Skills:** `.agents/skills/text-to-speech`, `.agents/skills/elevenlabs`,
`.agents/skills/azure-text-to-speech`, `skills/meta/voice-performance-director.md`

---

## Start With `voice-performance-director`

OpenMontage has a dedicated meta-skill for this: `skills/meta/voice-performance-director.md`.
**Read it before directing any voice performance.** It is the upstream answer to
"how should this be performed," and this file should not restate it.

## Route Through `tts_selector`

Do **not** hardcode a provider. `tts_selector` picks based on what's configured.

**Free/local first:** `piper_tts` needs no API key. For internal drafts and timing
tests, use it — save the paid voice for the take that ships.

## The Script Problem

TTS does not see meaning; it sees text. Punctuation is the entire performance
direction available to you.

| Want | Write |
|---|---|
| Pause | Comma, or `...` for longer |
| Hard stop | Period. |
| Lift in energy | Short sentence. Break the rhythm. |
| Emphasis | Rephrase so the word is sentence-final |
| Slower | Shorter clauses, more punctuation |
| Warmer | Contractions — "we're" not "we are" |

**Numbers and abbreviation:** verify how the provider reads them. `2026` may be read
as "two thousand twenty-six" or "twenty twenty-six". Test before a full render.
`$1.5M`, `Dr.`, `vs.`, and acronyms are all common surprises.

## Pace Target By Register

| Register | Words per minute | Feel |
|---|---|---|
| `urgent` | 165–185 | Energetic, forward |
| `steady` | 140–160 | Confident, clear |
| `calm` | 115–140 | Deliberate, considered |

TTS defaults usually land around 150 wpm. Adjust per chunk rather than globally —
a single rate across a whole script sounds mechanical.

## Entry Format

```markdown
### {{name}}
**Provider / tool:** {{real tool}}   **Voice ID:** {{id or "selector default"}}
**Cost:** {{per 1k chars}}

**Script with direction:**
{{the exact text, including punctuation that creates the performance}}

**Settings:** {{speed, stability, similarity, style if applicable}}

**Notes:** {{what you learned}}
```

## Rules

1. **Read `voice-performance-director.md` first.** Upstream provides it; use it.
2. **Draft with `piper_tts`, ship with the paid voice.**
3. **Test number/abbreviation reads before committing to a full render.**
4. **Match WPM to the declared register.**
5. **Chunk long scripts at sentence boundaries** and generate in parallel where the
   tool supports it. Single long calls fail more and are slower to iterate on.
6. **Listen to the whole thing.** TTS misreads are unpredictable and land in the
   worst places.
7. **Voice consistency across a project is mandatory** — same voice ID, same settings,
   every segment.

## Entries

_None yet._
