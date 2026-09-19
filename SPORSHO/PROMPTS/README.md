# PROMPTS — Your Prompt Library

Reusable prompts for generation stages.

---

## Relationship To Upstream

OpenMontage ships `PROMPT_GALLERY.md` (generic, project-authored). This folder is
**yours** — prompts tuned to your clients, your market, your taste.

Do not duplicate `PROMPT_GALLERY.md` here. If a prompt there works, reference it;
don't copy it. Copies go stale silently.

## The Critical Rule

**Before writing image/video/TTS prompts with any generation tool, read its Layer 3
skill.** Upstream's `AGENT_GUIDE.md` is emphatic about this:

> *"Every generation tool (video, image, TTS, music) has an `agent_skills` field
> listing its Layer 3 skills. These skills contain provider-specific prompt
> engineering, parameter tuning, and quality techniques. Read them before writing
> prompts. The difference between a generic prompt and a skill-informed prompt is the
> difference between 'usable' and 'cinematic.'"*

A prompt in this folder is a **starting point**. The provider skill tells you how to
adapt it. Never paste a generic prompt into a provider without reading its skill first.

---

## Files

| File | For |
|---|---|
| [`IMAGE-PROMPTS.md`](IMAGE-PROMPTS.md) | Still image generation |
| [`VIDEO-PROMPTS.md`](VIDEO-PROMPTS.md) | Video generation |
| [`VOICE-PROMPTS.md`](VOICE-PROMPTS.md) | TTS direction |
| [`MUSIC-PROMPTS.md`](VOICE-PROMPTS.md) | Music generation |

---

## Entry Format

```markdown
### {{name}}
**Tool:** {{real tool name}}   **Layer 3 skill read:** {{skill}}
**Use when:** {{trigger}}
**Cost:** {{if a paid provider}}

{{the prompt}}

**Notes:** {{what you learned using it — this is what makes it worth keeping}}
```

The **Notes** field is the valuable part. A prompt without usage notes is a snippet;
a prompt with notes is knowledge.

## Provider-Specific, Not Universal

Prompts do not transfer cleanly between providers. Kling, Seedance, Veo, and Sora
respond to different prompt structures. Keep prompts **grouped by provider**, and
record which one a prompt was tuned for.

Cheapest approach to a provider swap: read the new provider's Layer 3 skill, then
re-tune the prompt's *structure* while keeping the *intent*.

## What Belongs Here Vs. Elsewhere

| Belongs here | Belongs elsewhere |
|---|---|
| Provider prompt text | Client preferences → `CLIENTS/` |
| Parameter settings | General editing rules → `EDITING-RULES/` |
| Negative prompts | Look definition → `styles/custom/*.yaml` |
| Prompt-structure notes | Cross-project lessons → `MEMORY/` |

Look-and-feel (palette, type, motion language) is a **playbook**, not a prompt.
Playbooks go in `styles/custom/` where the render path can find them.
