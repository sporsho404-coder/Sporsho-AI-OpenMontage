# Image Prompts

**Tools:** `image_gen`, `image_selector`, `flux_image`, `openai_image`, `recraft_image`,
`seedream_image`, `google_imagen`, `fal_*`, `local_diffusion`

**Read first:** the Layer 3 skill for the provider you're using
(`.agents/skills/bfl-api`, `.agents/skills/flux-best-practices`, ...). Upstream requires
this before any generation call — see `AGENT_GUIDE.md` § Layer Map.

---

## Why Read The Skill First

Providers differ structurally. Flux responds to natural-language prose; others want
comma-separated tags; some honour explicit camera/lens vocabulary. A prompt tuned for
one provider underperforms badly on another. **The skill tells you the structure.**

## The Consistency Problem

The hardest part of AI image work is not one good image — it's **ten images that look
like they came from the same video.** OpenMontage addresses this via the playbook's
`consistency_anchors` array and `image_prompt_prefix`.

**Always define anchors before generating.** Put the invariant description in the
playbook, not in each prompt:

```yaml
asset_generation:
  image_prompt_prefix: "cinematic still, 35mm, shallow depth of field"
  image_negative_prompt: "text, watermark, extra fingers, deformed hands"
  consistency_anchors:
    - "cold blue-grey palette"
    - "soft directional key light from camera left"
    - "matte contrast, no blown highlights"
```

Every scene prompt then inherits those anchors. This is why `styles/custom/*.yaml`
exists — see `docs/sporsho/INTEGRATION.md` § 2.

## Entry Format

```markdown
### {{name}}
**Provider / tool:** {{real tool}}   **Layer 3 skill read:** {{skill}}
**Playbook:** {{styles/custom/*.yaml if used}}
**Use when:** {{trigger}}

**Prompt:**
{{prompt}}

**Negative:**
{{negative prompt}}

**Params:** {{aspect ratio, steps, guidance, seed}}

**Notes:** {{what you learned — the valuable part}}
```

## Aspect Ratio Cheat Sheet

| Deliverable | Ratio | Generate at |
|---|---|---|
| 9:16 short-form | 9:16 | 1080×1920 |
| 16:9 YouTube | 16:9 | 1920×1080 |
| Square social | 1:1 | 1080×1080 |
| B-roll insert, reframed later | 16:9 | generate wide, crop in edit |

**Generate wide, crop in.** You can always cut a 16:9 frame down to 9:16. You cannot
add back what was never generated.

## Rules

1. **Never generate an image you could shoot or source.** Stock is cheaper and faster
   for anything generic.
2. **Never generate before reading the provider skill.**
3. **Always record the prompt** that produced a keeper — put it in this file with notes.
4. **Always use `image_selector`** to choose among variants when multiple are generated.
5. **Never put text in a generated image.** Render typography in Remotion where it is
   crisp, controllable, and contrast-checkable.

## Entries

_None yet._ Add each keeper with its notes as you produce real work.
