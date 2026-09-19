# CAPABILITY MAP — What Exists vs. What Must Be Built

Every requirement you listed for this system, checked against the actual OpenMontage
source at commit `08e2151`. **Nothing here is assumed.**

Legend:
- ✅ **EXISTS** — implemented upstream, use it
- ⚠️ **PARTIAL** — exists but doesn't fully cover the requirement
- ❌ **MISSING** — does not exist; Sporsho must supply it

---

## Your Requirements, Checked

| # | Requirement | Status | Evidence |
|---|---|---|---|
| 1 | Reference-video analysis | ✅ | `skills/meta/video-reference-analyst.md`, `tools/analysis/video_analyzer.py`, "Reference Video Entry Point" in `AGENT_GUIDE.md` |
| 2 | Reference-based editing decisions | ✅ | Same, plus 5-aspect breakdown designed for downstream lifting |
| 3 | Talking-head editing | ✅ | `pipeline_defs/talking-head.yaml` (**beta**), `skills/creative/video-editing.md` |
| 4 | Short-form 9:16 editing | ✅ | `tools/video/auto_reframe.py`, 95 files reference `9:16` |
| 5 | B-roll selection | ✅ | `skills/creative/broll-planning.md`, `clip_search`, `direct_clip_search`, `pexels_video`, `pixabay_video` |
| 6 | Pacing | ✅ | `skills/creative/video-editing.md`, `skills/creative/video-stitching.md`, `lib/verify_scene_pacing.py` |
| 7 | Cuts | ✅ | `tools/video/video_trimmer.py`, `tools/video/silence_cutter.py` |
| 8 | J-cuts / L-cuts | ✅ | `skills/creative/video-editing.md` L35–36, `video-stitching.md` L155–156, `documentary-montage/compose-director.md` |
| 9 | Captions | ✅ | `tools/subtitle/subtitle_gen.py`, `tools/video/remotion_caption_burn.py`, `skills/core/subtitle-sync.md` |
| 10 | Typography | ✅ | `skills/creative/typography.md`, playbook `typography` schema with type scales |
| 11 | Motion graphics | ✅ | `pipeline_defs/animation.yaml`, `.agents/skills/gsap-*`, `framer-motion`, `lottie-bodymovin`, `manim-*` |
| 12 | Music | ✅ | `tools/audio/music_gen.py` + 6 more music tools; `skills/creative/sound-design.md` |
| 13 | Sound design | ✅ | `skills/creative/sound-design.md`, `.agents/skills/sound-effects` |
| 14 | Visual consistency | ✅ | `lib/variation_checker.py`, `lib/slideshow_risk.py`, playbook `consistency_anchors` |
| 15 | **Client-specific editing rules** | ❌ | **Zero references to client profiles in source.** Sporsho supplies: `SPORSHO/CLIENTS/` |
| 16 | **Revision handling** | ❌ | Upstream `max_revisions_per_stage` is *stage send-backs*, not client rounds. Sporsho supplies: `CLIENTS/*/REVISION-LOG.md`, `WORKFLOWS/REVISION-ROUND.md` |
| 17 | Final quality control | ✅ | `skills/meta/reviewer.md` (CHAI rules), `tools/analysis/visual_qa.py`, `lib/delivery_promise.py` |
| 18 | **Learning from successful/failed edits** | ❌ | No retrospective artifact or lessons store upstream. Sporsho supplies: `SPORSHO/MEMORY/` |
| 19 | Reusable editing workflows | ⚠️ | 13 pipeline manifests exist; they are *generic*. Sporsho supplies client-bound recipes: `SPORSHO/WORKFLOWS/` |
| 20 | **Multiple client profiles** | ❌ | Does not exist. Sporsho supplies: `SPORSHO/CLIENTS/` |
| 21 | **Project-specific instructions** | ⚠️ | Project dirs exist but are gitignored and regenerable — no persistent per-project instruction store. Sporsho supplies: `CLIENTS/` + `WORKFLOWS/` |

**Score: 15 of 21 fully exist. 2 partial. 4 genuinely missing.**

The four missing items are exactly what the Sporsho layer is for. That is the whole
point of this architecture — and it is why Sporsho *configures* rather than rebuilds.

---

## What OpenMontage Has That You Didn't Ask For

Worth knowing about, because they expand what's possible:

| Capability | Where |
|---|---|
| 13 end-to-end pipelines | `pipeline_defs/` |
| ~100 tools across 12 families | `tools/` |
| ~110 Layer-2 skills (how to use tools) | `skills/` |
| ~85 Layer-3 vendor skills | `.agents/skills/` |
| Multi-provider video generation (20+ providers) | `tools/video/` |
| Avatar / lip-sync | `tools/avatar/` |
| Localisation & dubbing | `pipeline_defs/localization-dub.yaml` |
| Screen recording (real & synthetic) | `tools/capture/`, `.agents/skills/synthetic-screen-recording` |
| 3D world generation | `tools/graphics/blender_world.py`, `atlas_3d` |
| Character rigging & animation | `tools/character/`, `.agents/skills/character-rigging` |
| Documentaries / montage | `pipeline_defs/documentary-montage.yaml` |
| Podcast repurposing | `pipeline_defs/podcast-repurpose.yaml` |
| A live production board UI | `backlot/` |
| Cost tracking & budget gates | `tools/cost_tracker.py`, `config.yaml` budget block |
| Accessibility validators (WCAG, colour-blind) | `lib/playbook_loader.py` |
| 3-layer instruction architecture | `tools/` → `skills/` → `.agents/skills/` |
| 449 commits of upstream history | preserved in this repo |

---

## The Three-Layer Instruction Model (Upstream's Best Idea)

Worth understanding, because it determines where you put things:

| Layer | Question it answers | Location |
|---|---|---|
| 1 | **What exists?** — availability, cost, runtime, fallback | `tools/` registry |
| 2 | **How should it be used *here*?** — pipeline context | `skills/` |
| 3 | **How does the vendor tool actually work?** | `.agents/skills/` |

Reading order is 1 → 2 → 3. Upstream requires Layer 3 to be read **before calling any
generation tool** — those files hold provider-specific prompt engineering and
parameter tuning.

**Where Sporsho fits:** above all three, as a fourth layer that says *what the client
wants and what we learned*. It constrains layers 1–3; it never replaces them.

---

## Honest Limits

Things that are genuinely constrained, so you don't plan around them:

1. **Beta pipelines.** `talking-head`, `clip-factory`, `podcast-repurpose`,
   `character-animation`, `localization-dub` are not fully audited upstream. They work,
   with rough edges.

2. **The `extensions:` flags don't resolve.** Declared in YAML, not implemented in code.
   Adding a file to `SPORSHO/` does not make a pipeline pick it up.

3. **No custom pipeline discovery.** `load_pipeline(defs_dir=)` exists, but no CLI
   wires it. You must call it yourself.

4. **MCP is HeyGen-only.** No general MCP framework.

5. **Memory is a contract, not code.** Nothing enforces writing lessons. It works if
   you keep entries short enough to actually write.

6. **Provider availability depends on your API keys.** A tool in the registry may not
   be callable. **Always check configuration before promising a provider** — this is
   the single most common false promise in generated plans.

7. **AGPL-3.0.** See `INTEGRATION.md` § The AGPL-3.0 Question.
