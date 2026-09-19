# Video Prompts

**Tools:** `kling_video`, `kling_official_video`, `seedance_video`, `seedance_ark`,
`seedance_replicate`, `veo_video`, `sora_video`, `runway_video`, `minimax_video`,
`hunyuan_video`, `wan_video`, `ltx_video_local`, `cogvideo_video`, `grook_video`,
`jimeng_video`, `higgsfield_video`, `comfyui_video`

**Read first:** the Layer 3 skill — `.agents/skills/ai-video-gen`, `seedance-2-0`,
`gemini-omni`, `ltx2`, `kling-official`.

---

## Upstream's Own Warning

From `AGENT_GUIDE.md` § Layer Map:

> *"Before calling `kling_video`, read its `agent_skills` → `ai-video-gen` → get
> Kling-specific prompt structure, camera direction syntax, and quality keywords that
> the model responds to best."*

And:

> *"The difference between a generic prompt and a skill-informed prompt is the
> difference between 'usable' and 'cinematic.'"*

Do not skip this. It is the single highest-leverage habit in video generation.

## Cost Reality

Video generation is the most expensive operation in this system. Before any call:

- [ ] Is a generated clip actually needed here, or would stock work?
      (`direct_clip_search`, `pexels_video`, `pixabay_video` are far cheaper)
- [ ] Is the budget confirmed with the user?
- [ ] Does `config.yaml` `single_action_approval_usd` require approval?
- [ ] Are you generating once, or iterating? Iteration multiplies cost.

**Cheapest path that still works wins.** Generated video is a deliberate choice, not a default.

## Entry Format

```markdown
### {{name}}
**Provider / tool:** {{real tool}}   **Layer 3 skill read:** {{skill}}
**Cost:** {{per clip / per second}}
**Use when:** {{trigger}}

**Prompt:**
{{prompt}}

**Params:** {{duration, aspect, resolution, motion strength, seed}}

**Notes:** {{what worked, what wasted money}}
```

## Prompt Structure

Most video models respond to this order. Provider skills refine it:

```
[subject + action] → [setting] → [camera: movement, shot size, angle, lens] →
[lighting] → [style/grade] → [motion quality] → [duration/pace hint]
```

Camera vocabulary matters more in video than in stills — it is what creates the
sensation of a *shot* rather than an animation of a picture.

## Rules

1. **Read the provider skill before writing the prompt.** Non-negotiable.
2. **Start with the cheapest provider that can achieve the look.** Escalate only if it fails.
3. **Generate short, extend in edit.** Most models degrade past their natural clip
   length; also cheaper to test.
4. **Keep clips 3–5s** unless the shot genuinely needs longer. Cuts are cheaper than
   long takes.
5. **Match the declared register.** `urgent` wants energy and movement; `calm` wants
   slow, deliberate camera.
6. **Never generate a talking head** — use `avatar-spokesperson` or real footage.
7. **Record every failed prompt.** Failed prompts are the most valuable entries here —
   they stop you spending the same money twice.

## Entries

_None yet._ Add entries as you produce real work, including failures.
